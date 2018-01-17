import re

from livecli import NoPluginError
from livecli import PluginError
from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.utils import update_scheme


class APac(Plugin):
    url_re = re.compile(r"https?://(?:www\.)?a-pac\.tv/")
    iframe_re = re.compile(r'<iframe.*?src="([^"]+)".*?></iframe>')

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        res = http.get(self.url)
        # Search for the iframe in the page
        iframe_m = self.iframe_re.search(res.text)

        ustream_url = iframe_m and iframe_m.group(1)
        if ustream_url and "ustream.tv" in ustream_url:
            try:
                ustream_url = update_scheme(self.url, ustream_url)
                return self.session.streams(ustream_url)
            except NoPluginError:
                raise PluginError("Could not play embedded stream: {0}".format(ustream_url))


__plugin__ = APac
