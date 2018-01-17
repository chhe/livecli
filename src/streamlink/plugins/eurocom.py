from __future__ import print_function
import re

from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.stream import RTMPStream


class Eurocom(Plugin):
    url_re = re.compile(r"https?://(?:www\.)?eurocom.bg/live/?")
    file_re = re.compile(r"file:.*?(?P<q>['\"])(?P<url>rtmp://[^\"']+)(?P=q),")

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        res = http.get(self.url)
        m = self.file_re.search(res.text)
        if m:
            stream_url = m.group("url")
            yield "live", RTMPStream(self.session, params={"rtmp": stream_url})


__plugin__ = Eurocom
