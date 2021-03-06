# -*- coding: utf-8 -*-
import json
import re
import time

from datetime import datetime
from threading import Thread
from threading import Timer
from websocket import create_connection

from livecli.cache import Cache
from livecli.exceptions import PluginError
from livecli.plugin import Plugin
from livecli.plugin import PluginOptions
from livecli.plugin.api import http
from livecli.plugin.api import useragents
from livecli.plugin.api import validate
from livecli.stream import RTMPStream
from livecli.utils import filter_urlquery

__livecli_docs__ = {
    'domains': [
        'live.fc2.com',
    ],
    'geo_blocked': [],
    'notes': '',
    'live': True,
    'vod': False,
    'last_update': '2018-05-02',
}


class FC2(Plugin):
    '''Livecli Plugin for live.fc2.com'''

    url_login = 'https://secure.id.fc2.com/?mode=login&switch_language=en'
    url_member_api = 'https://live.fc2.com/api/memberApi.php'
    url_server = 'https://live.fc2.com/api/getControlServer.php'

    _url_re = re.compile(r'''https?://live\.fc2\.com/(?P<user_id>\d+)/?$''')

    count = 0
    count_ping = 0

    _version_schema = validate.Schema({
        'status': int,
        'data': {
            'channel_data': {
                'channelid': validate.text,
                'userid': validate.text,
                'adult': int,
                'login_only': int,
                'version': validate.text,
                'fee': int,
            },
            'user_data': {
                'is_login': int,
                'userid': int,
                'fc2id': int,
                'name': validate.text,
                'point': int,
                'adult_access': int,
                'recauth': int,
            }
        }
    })

    host_data = ''
    host_found = False

    expires_time = 3600 * 24

    options = PluginOptions({
        'username': None,
        'password': None,
        'purge_credentials': None
    })

    def __init__(self, url):
        super(FC2, self).__init__(url)
        self._session_attributes = Cache(filename='plugin-cache.json', key_prefix='fc2:attributes')
        self._authed = (self._session_attributes.get('fcu')
                        and self._session_attributes.get('fgcv')
                        and self._session_attributes.get('FCSID')
                        and self._session_attributes.get('login_status')
                        and self._session_attributes.get('glgd_val')
                        and self._session_attributes.get('PHPSESSID')
                        and self._session_attributes.get('secure_check_fc2'))
        self._expires = self._session_attributes.get('expires', time.time() + self.expires_time)

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def set_expires_time_cache(self):
        expires = time.time() + self.expires_time
        self._session_attributes.set('expires', expires, expires=self.expires_time)

    def _login(self, username, password):
        '''login and update cached cookies'''
        self.logger.debug('login ...')
        http.get(self.url)
        data = {
            'pass': password,
            'email': username,
            'done': 'livechat',
            'keep_login': 1
        }

        http.post(self.url_login, data=data, allow_redirects=True)
        for cookie in http.cookies:
            self._session_attributes.set(cookie.name, cookie.value, expires=3600 * 24)

        if (self._session_attributes.get('fcu')
           and self._session_attributes.get('fgcv')
           and self._session_attributes.get('FCSID')
           and self._session_attributes.get('login_status')
           and self._session_attributes.get('glgd_val')
           and self._session_attributes.get('PHPSESSID')
           and self._session_attributes.get('secure_check_fc2')):

            self.logger.debug('New session data')
            self.set_expires_time_cache()
            return True
        else:
            self.logger.error('Failed to login, check your username/password')
            return False

    def _get_version(self, user_id):
        data = {
            'user': 1,
            'channel': 1,
            'profile': 1,
            'streamid': int(user_id)
        }
        res = http.post(self.url_member_api, data=data)
        res_data = http.json(res, schema=self._version_schema)
        channel_data = res_data['data']['channel_data']
        user_data = res_data['data']['user_data']

        if (channel_data['login_only'] != 0 and user_data['is_login'] != 1):
            raise PluginError('A login is required for this stream.')

        if channel_data['fee'] != 0:
            raise PluginError('Only streams without a fee are supported by Livecli.')

        version = channel_data['version']
        if user_data['is_login']:
            self.logger.info('Logged in as {0}'.format(user_data['name']))
        self.logger.debug('Found version: {0}'.format(version))
        return version

    def payload_msg(self, name):
        ''' Format the WebSocket message '''
        self.count_ping += 1
        payload = json.dumps(
            {
                'name': str(name),
                'arguments': {},
                'id': int(self.count_ping)
            }
        )
        return payload

    def _get_ws_url(self, user_id, version):
        self.logger.debug('_get_ws_url ...')
        data = {
            'channel_id': user_id,
            'channel_version': version,
            'client_type': 'pc',
            'client_app': 'browser'
        }

        res = http.post(self.url_server, data=data)
        w_data = http.json(res)
        if w_data['status'] == 11:
            raise PluginError('The broadcaster is currently not available')

        new_dict = {
            'control_token': w_data['control_token'],
            'mode': 'pay',
            'comment': '0',
        }
        ws_url = filter_urlquery(w_data['url'], new_dict=new_dict)
        self.logger.debug('WS URL: {0}'.format(ws_url))
        return ws_url

    def _get_ws_data(self, ws_url):
        self.logger.debug('_get_ws_data ...')
        ws = create_connection(ws_url)
        ws.send(self.payload_msg('get_media_server_information'))

        def ws_ping():
            ''' ping the WebSocket '''
            if ws.connected is True:
                t1 = Timer(30.0, ws_ping)
                t1.daemon = True
                t1.start()
                ws.send(self.payload_msg('heartbeat'))

        def ws_recv():
            ''' print WebSocket messages '''
            while True:
                self.count += 1
                data = json.loads(ws.recv())
                time_utc = datetime.utcnow().strftime('%H:%M:%S UTC')
                if data['name'] not in ['comment', 'ng_commentq', 'user_count', 'ng_comment']:
                    self.logger.debug('{0} - {1} - {2}'.format(time_utc, self.count, data['name']))

                if data['name'] == '_response_' and data['arguments'].get('host'):
                    self.logger.debug('Found host data')
                    self.host_data = data
                    self.host_found = True
                elif data['name'] == 'media_connection':
                    self.logger.debug('successfully opened stream')
                elif data['name'] == 'control_disconnection':
                    break
                elif data['name'] == 'publish_stop':
                    self.logger.debug('Stream ended')
                elif data['name'] == 'channel_information':
                    if data['arguments'].get('fee') != 0:
                        self.logger.error('Stream requires a fee now, this is not supported by Livecli.'.format(data['arguments'].get('fee')))
                        break

            ws.close()

        # WebSocket background process
        ws_ping()
        t2 = Thread(target=ws_recv)
        t2.daemon = True
        t2.start()

        # wait for the WebSocket
        host_timeout = False
        while self.host_found is False:
            if self.host_found is True:
                break
            if self.count >= 30:
                host_timeout = False

        if host_timeout:
            return False
        return True

    def _get_rtmp(self, data):
        self.logger.debug('_get_rtmp ...')

        app = filter_urlquery(data['application'],
                              new_dict={'media_token': data['media_token']})
        host = data['host']

        params = {
            'app': app,
            'flashVer': 'WIN 29,0,0,140',
            'swfUrl': 'https://live.fc2.com/swf/liveVideo.swf',
            'tcUrl': 'rtmp://{0}/{1}'.format(host, app),
            'live': 'yes',
            'pageUrl': self.url,
            'playpath': data['play_rtmp_stream'],
            'host': host,
        }
        yield 'live', RTMPStream(self.session, params)

    def _get_streams(self):
        http.headers.update({
            'User-Agent': useragents.FIREFOX,
            'Referer': self.url
        })

        login_username = self.get_option('username')
        login_password = self.get_option('password')

        if self.options.get('purge_credentials'):
            self._session_attributes.set('fcu', None, expires=0)
            self._session_attributes.set('fgcv', None, expires=0)
            self._session_attributes.set('FCSID', None, expires=0)
            self._session_attributes.set('login_status', None, expires=0)
            self._session_attributes.set('glgd_val', None, expires=0)
            self._session_attributes.set('PHPSESSID', None, expires=0)
            self._session_attributes.set('secure_check_fc2', None, expires=0)
            self._authed = False
            self.logger.info('All credentials were successfully removed.')

        if self._authed:
            if self._expires < time.time():
                self.logger.debug('get new cached cookies')
                # login after 24h
                self.set_expires_time_cache()
                self._authed = False
            else:
                self.logger.info('Attempting to authenticate using cached cookies')
                http.cookies.set('fcu', self._session_attributes.get('fcu'))
                http.cookies.set('fgcv', self._session_attributes.get('fgcv'))
                http.cookies.set('FCSID', self._session_attributes.get('FCSID'))
                http.cookies.set('login_status', self._session_attributes.get('login_status'))
                http.cookies.set('glgd_val', self._session_attributes.get('glgd_val'))
                http.cookies.set('PHPSESSID', self._session_attributes.get('PHPSESSID'))
                http.cookies.set('secure_check_fc2', self._session_attributes.get('secure_check_fc2'))

        if (not self._authed and login_username and login_password):
            self._login(login_username, login_password)

        match = self._url_re.match(self.url)
        if not match:
            return

        user_id = match.group('user_id')

        version = self._get_version(user_id)
        ws_url = self._get_ws_url(user_id, version)
        if self._get_ws_data(ws_url):
            return self._get_rtmp(self.host_data['arguments'])


__plugin__ = FC2
