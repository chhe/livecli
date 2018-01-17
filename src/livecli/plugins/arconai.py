import re

from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.plugin.api import useragents
from livecli.stream import HLSStream

_url_re = re.compile(r'''https?://(www\.)?arconaitv\.co/stream\.php\?id=\d+''')
_playlist_re = re.compile(r'''source\ssrc=["'](?P<url>[^"']+)["']''')


class ArconaiTv(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):
        headers = {
            'User-Agent': useragents.CHROME,
            'Referer': self.url
        }

        res = http.get(self.url, headers=headers)

        match = _playlist_re.search(res.text)
        if match is None:
            return

        url = match.group('url')

        if url:
            self.logger.debug('HLS URL: {0}'.format(url))
            yield 'live', HLSStream(self.session, url, headers=headers)


__plugin__ = ArconaiTv
