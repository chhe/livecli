# -*- coding: utf-8 -*-
import re

from livecli import NoPluginError
from livecli import NoStreamsError
from livecli.compat import unquote
from livecli.compat import urljoin
from livecli.compat import urlparse
from livecli.plugin import Plugin
from livecli.plugin import PluginOptions
from livecli.plugin.api import http
from livecli.plugin.api import useragents
from livecli.plugin.plugin import HIGH_PRIORITY
from livecli.plugin.plugin import NO_PRIORITY
from livecli.stream import HDSStream
from livecli.stream import HLSStream
from livecli.stream import HTTPStream
from livecli.utils import update_scheme
from livecli.plugin.api.common import _iframe_re
from livecli.plugin.api.common import _playlist_re
from livecli.plugin.api.common import _rtmp_re


class ResolveCache:
    """used as temporary url cache
       - ResolveCache.cache_url_list
    """
    pass


class Resolve(Plugin):
    """Plugin that will try to find a valid streamurl on every website

    Supported
        - embedded url of an already existing plugin
        - website with an unencrypted fileurl in there source code,
          HDS, HLS and HTTP

    Unsupported
        - websites with DASH or RTMP
          it will show the url in the debug log, but won't try to start it.
        - streams that require
            - an authentication
            - an API
        - streams that are hidden behind javascript or other encryption
    """

    _url_re = re.compile(r"""(resolve://)?(?P<url>.+)""")
    # Regex for: .mp3 and mp4 files
    _httpstream_bitrate_re = re.compile(r"""_(?P<bitrate>\d{1,4})\.mp(?:3|4)""")
    # Regex for: streamBasePath for .f4m urls
    _stream_base_re = re.compile(r"""streamBasePath\s?(?::|=)\s?["'](?P<base>[^"']+)["']""", re.IGNORECASE)
    # Regex for: javascript redirection
    _window_location_re = re.compile(r"""<script[^<]+window\.location\.href\s?=\s?["'](?P<url>[^"']+)["'];[^<>]+""", re.DOTALL)
    _unescape_iframe_re = re.compile(r"""unescape\(["'](?P<data>%3C(?:iframe|%69%66%72%61%6d%65)%20[^"']+)["']""", re.IGNORECASE)
    # Regex for obviously ad paths
    _ads_path = re.compile(r"""(?:/static)?/ads?/?(?:\w+)?(?:\d+x\d+)?(?:_\w+)?\.(?:html?|php)""")

    # START - _make_url_list
    # Allow only a valid scheme, after the url was repaired
    valid_scheme = (
        "http",
    )
    # Not allowed at the end of the parsed url path
    blacklist_endswith = (
        ".gif",
        ".jpg",
        ".png",
        ".svg",
        ".vtt",
        "/chat.html",
        "/chat",
    )
    # Not allowed at the end of the parsed url netloc
    blacklist_netloc = (
        "127.0.0.1",
        "about:blank",
        "abv.bg",
        "adfox.ru",
        "googletagmanager.com",
        "javascript:false",
    )
    # Not allowed at the end of the parsed url netloc and the start of the path
    blacklist_path = [
        ("expressen.se", "/_livetvpreview/"),
        ("facebook.com", "/connect"),
        ("facebook.com", "/plugins"),
        ("haber7.com", "/radyohome/station-widget/"),
        ("static.tvr.by", "/upload/video/atn/promo"),
        ("twitter.com", "/widgets"),
        ("vesti.ru", "/native_widget.html"),
    ]
    # Only allowed as a valid file format in playlist urls
    whitelist_endswith = (
        ".f4m",
        ".hls",
        ".m3u",
        ".m3u8",
        ".mp3",
        ".mp4",
        ".mpd",
    )
    # END - _make_url_list

    # PluginOptions
    options = PluginOptions({
        "turn_off": False,
        "blacklist_netloc": None,
        "blacklist_path": None,
        "whitelist_netloc": None,
        "whitelist_path": None,
    })

    def __init__(self, url):
        super(Resolve, self).__init__(url)
        # Remove prefix
        self.url = self.url.replace("resolve://", "")
        # cache every used url, this will avoid a loop
        if hasattr(ResolveCache, "cache_url_list"):
            ResolveCache.cache_url_list += [self.url]
            # set the last url as a referer
            self.referer = ResolveCache.cache_url_list[-2]
        else:
            ResolveCache.cache_url_list = [self.url]
            self.referer = self.url

        # default GET header
        self.headers = {
            "User-Agent": useragents.FIREFOX,
            "Referer": self.referer
        }

    @classmethod
    def priority(cls, url):
        """
        Returns
        - NO priority if the URL is not prefixed
        - HIGH priority if the URL is prefixed
        :param url: the URL to find the plugin priority for
        :return: plugin priority for the given URL
        """
        m = cls._url_re.match(url)
        if m:
            prefix, url = cls._url_re.match(url).groups()
            if prefix is None:
                return NO_PRIORITY
            elif prefix is not None:
                return HIGH_PRIORITY
        return NO_PRIORITY

    @classmethod
    def can_handle_url(cls, url):
        m = cls._url_re.match(url)
        if m and cls.get_option("turn_off") is False:
            return m.group("url") is not None

    def help_info_e(self, e):
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            self.logger.info("A workaround for this error is --http-no-ssl-verify "
                             "https://livecli.github.io/cli.html#cmdoption-http-no-ssl-verify")
        return

    def compare_url_path(self, parsed_url, check_list):
        """compare a parsed url, if it matches an item from a list

        Args:
           parsed_url: a url that was used with urlparse
           check_list: a list of urls that should get checked

        Returns:
            True
                if parsed_url in check_list
            False
                if parsed_url not in check_list
        """
        status = False
        for netloc, path in check_list:
            if parsed_url.netloc.endswith(netloc) and parsed_url.path.startswith(path):
                status = True
        return status

    def merge_path_list(self, static_list, user_list):
        """merge the static list, with an user list

        Args:
           static_list: static list from this plugin
           user_list: list from a user command

        Returns:
            A new valid static_list
        """
        for _path_url in user_list:
            if not _path_url.startswith(("http", "//")):
                _path_url = update_scheme("http://", _path_url)
            _parsed_path_url = urlparse(_path_url)
            if _parsed_path_url.netloc and _parsed_path_url.path:
                static_list += [(_parsed_path_url.netloc, _parsed_path_url.path)]
        return static_list

    def _make_url_list(self, old_list, base_url, url_type="", stream_base=""):
        """creates a list of valid urls
           - repairs urls
           - removes unwanted urls

        Args:
            old_list: list of urls
            base_url: url that will get used for scheme and netloc repairs
            url_type: can be ... and is used for ...
                - iframe
                    --resolve-whitelist-netloc
                - playlist
                    whitelist_endswith
            stream_base: basically same as base_url, but used for .f4m files.

        Returns:
            New list of validate urls.
        """

        blacklist_netloc_user = self.get_option("blacklist_netloc")
        whitelist_netloc_user = self.get_option("whitelist_netloc")

        # repairs scheme of --resolve-blacklist-path and merges it into blacklist_path
        blacklist_path_user = self.get_option("blacklist_path")
        if blacklist_path_user is not None:
            self.blacklist_path = self.merge_path_list(self.blacklist_path, blacklist_path_user)

        # repairs scheme of --resolve-whitelist-path and merges it into whitelist_path
        whitelist_path_user = self.get_option("whitelist_path")
        if whitelist_path_user is not None:
            whitelist_path = self.merge_path_list([], whitelist_path_user)

        new_list = []
        for url in old_list:
            # Repair the scheme
            new_url = url.replace("\\", "")
            # repairs broken scheme
            if new_url.startswith("http&#58;//"):
                new_url = "http:" + new_url[9:]
            elif new_url.startswith("https&#58;//"):
                new_url = "https:" + new_url[10:]
            # creates a valid url from path only urls and adds missing scheme for // urls
            if stream_base and new_url[1] is not "/":
                if new_url[0] is "/":
                    new_url = new_url[1:]
                new_url = urljoin(stream_base, new_url)
            else:
                new_url = urljoin(base_url, new_url)
            # parse the url
            parse_new_url = urlparse(new_url)

            # START - removal of unwanted urls
            REMOVE = False

            # sorted after the way livecli will try to remove an url
            status_remove = [
                "SAME-URL",   # - Removes an already used iframe url
                "SCHEME",     # - Allow only an url with a valid scheme
                "WL-netloc",  # - Allow only whitelisted domains --resolve-whitelist-netloc
                "WL-path",    # - Allow only whitelisted paths from a domain --resolve-whitelist-path
                "BL-static",  # - Removes blacklisted domains
                "BL-netloc",  # - Removes blacklisted domains --resolve-blacklist-netloc
                "BL-path",    # - Removes blacklisted paths from a domain --resolve-blacklist-path
                "BL-ew",      # - Removes unwanted endswith images and chatrooms
                "WL-ew",      # - Allow only valid file formats for playlists
                "ADS",        # - Remove obviously ad urls
            ]

            if REMOVE is False:
                count = 0
                for url_status in ((new_url in ResolveCache.cache_url_list),
                                   (not parse_new_url.scheme.startswith(self.valid_scheme)),
                                   (url_type == "iframe" and
                                    whitelist_netloc_user is not None and
                                    parse_new_url.netloc.endswith(tuple(whitelist_netloc_user)) is False),
                                   (url_type == "iframe" and
                                    whitelist_path_user is not None and
                                    self.compare_url_path(parse_new_url, whitelist_path) is False),
                                   (parse_new_url.netloc.endswith(self.blacklist_netloc)),
                                   (blacklist_netloc_user is not None and
                                    parse_new_url.netloc.endswith(tuple(blacklist_netloc_user))),
                                   (self.compare_url_path(parse_new_url, self.blacklist_path) is True),
                                   (parse_new_url.path.endswith(self.blacklist_endswith)),
                                   ((url_type == "playlist" and
                                     not parse_new_url.path.endswith(self.whitelist_endswith))),
                                   (self._ads_path.match(parse_new_url.path))):

                    count += 1
                    if url_status:
                        REMOVE = True
                        break

            if REMOVE is True:
                self.logger.debug("{0} - Removed: {1}".format(status_remove[count - 1], new_url))
                continue
            # END - removal of unwanted urls

            # Add repaired url
            new_list += [new_url]
        # Remove duplicates
        new_list = list(set(new_list))
        return new_list

    def _iframe_src(self, res):
        """Try to find every iframe url,
           it will use the first iframe as self.url,
           but every other url will be shown in the terminal.

        Args:
            res: Content from self._res_text

        Returns:
            True
                if self.url was changed with an iframe url.
            None
                if no iframe was found.
        """
        iframe_all = _iframe_re.findall(res)

        # Fallback for unescape('%3Ciframe%20
        unescape_iframe = self._unescape_iframe_re.findall(res)
        if unescape_iframe:
            unescape_text = []
            for data in unescape_iframe:
                unescape_text += [unquote(data)]
            unescape_text = ",".join(unescape_text)
            unescape_iframe = _iframe_re.findall(unescape_text)
            if unescape_iframe:
                iframe_all = iframe_all + unescape_iframe

        if iframe_all:
            iframe_list = self._make_url_list(iframe_all, self.url, url_type="iframe")
            if iframe_list:
                self.logger.info("Found iframes: {0}".format(", ".join(iframe_list)))
                self.url = iframe_list[0]
                return True
        return None

    def _window_location(self, res):
        """Try to find a script with window.location.href

        Args:
            res: Content from self._res_text

        Returns:
            True
                if self.url was changed.
            None
                if no url was found.
        """

        match = self._window_location_re.search(res)
        if match:
            self.url = match.group("url")
            return True
        return None

    def _resolve_playlist(self, playlist_all):
        """ yield for _resolve_res

        Args:
            playlist_all: List of streams

        Returns:
            yield every stream
        """
        self.headers.update({"Referer": self.url})
        for url in playlist_all:
            parsed_url = urlparse(url)
            if parsed_url.path.endswith((".m3u8")):
                try:
                    streams = HLSStream.parse_variant_playlist(self.session, url, headers=self.headers).items()
                    if not streams:
                        yield "live", HLSStream(self.session, url, headers=self.headers)
                    for s in streams:
                        yield s
                except Exception as e:
                    self.logger.error("Skipping hls_url - {0}".format(str(e)))
                    self.help_info_e(e)
            elif parsed_url.path.endswith((".f4m")):
                try:
                    for s in HDSStream.parse_manifest(self.session, url, headers=self.headers).items():
                        yield s
                except Exception as e:
                    self.logger.error("Skipping hds_url - {0}".format(str(e)))
                    self.help_info_e(e)
            elif parsed_url.path.endswith((".mp3", ".mp4")):
                try:
                    name = "live"
                    m = self._httpstream_bitrate_re.search(url)
                    if m:
                        name = "{0}k".format(m.group("bitrate"))
                    yield name, HTTPStream(self.session, url, headers=self.headers)
                except Exception as e:
                    self.logger.error("Skipping http_url - {0}".format(str(e)))
                    self.help_info_e(e)
            elif parsed_url.path.endswith((".mpd")):
                try:
                    self.logger.info("Found mpd: {0}".format(url))
                except Exception as e:
                    self.logger.error("Skipping mpd_url - {0}".format(str(e)))
                    self.help_info_e(e)

    def _resolve_res(self, res):
        """find every playlist url on this website.

        Args:
            res: Content from self._res_text

        Returns:
            A list of stream urls
              or
            False
              - if no stream got added
        """
        playlist_all = _playlist_re.findall(res)

        # experimental rtmp search, will only print the url.
        m_rtmp = _rtmp_re.search(res)
        if m_rtmp:
            self.logger.info("Found RTMP: {0}".format(m_rtmp.group("url")))

        if playlist_all:
            # m_base is used for .f4m files that doesn't have a base_url
            m_base = self._stream_base_re.search(res)
            if m_base:
                stream_base = m_base.group("base")
            else:
                stream_base = ""

            playlist_list = self._make_url_list(playlist_all, self.url, url_type="playlist", stream_base=stream_base)
            if playlist_list:
                self.logger.debug("Found URL: {0}".format(", ".join(playlist_list)))
                return playlist_list
        return False

    def _res_text(self, url):
        """Content of a website

        Args:
            url: URL with an embedded Video Player.

        Returns:
            Content of the response
        """
        try:
            res = http.get(url, headers=self.headers, allow_redirects=True)
        except Exception as e:
            if "Received response with content-encoding: gzip" in str(e):
                headers = {
                    "User-Agent": useragents.FIREFOX,
                    "Referer": self.referer,
                    "Accept-Encoding": "deflate"
                }
                res = http.get(url, headers=headers, allow_redirects=True)
            elif "403 Client Error" in str(e):
                self.logger.error("Website Access Denied/Forbidden, you might be geo-blocked or other params are missing.")
                raise NoStreamsError(self.url)
            elif "404 Client Error" in str(e):
                self.logger.error("Website was not found, the link is broken or dead.")
                raise NoStreamsError(self.url)
            else:
                raise e

        if res.history:
            for resp in res.history:
                self.logger.debug("Redirect: {0} - {1}".format(resp.status_code, resp.url))
            self.logger.debug("URL: {0}".format(res.url))
        return res.text

    def _get_streams(self):
        """Try to find streams.

        Returns:
            Playable video
                or
            New self.url
        Raises:
            NoPluginError: if no video was found.
        """
        self.logger.debug("start resolve.py ...")
        self.url = update_scheme("http://", self.url)

        # GET website content
        o_res = self._res_text(self.url)

        # Video URL
        x = self._resolve_res(o_res)
        if x:
            return self._resolve_playlist(x)

        # iFrame URL
        x = self._iframe_src(o_res)

        if not x:
            # search for window.location.href
            x = self._window_location(o_res)

        if x:
            return self.session.streams(self.url)

        raise NoPluginError


__plugin__ = Resolve
