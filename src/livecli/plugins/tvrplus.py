import re

from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.plugin.api import validate
from livecli.stream import HLSStream


class TVRPlus(Plugin):
    url_re = re.compile(r"https?://(?:www\.)tvrplus.ro/live-")
    hls_file_re = re.compile(r"""src:\s?(?P<q>["'])(?P<url>http.+?m3u8.*?)(?P=q)""")

    stream_schema = validate.Schema(
        validate.all(
            validate.transform(hls_file_re.search),
            validate.any(None, validate.get("url"))
        ),
    )

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        stream_url = self.stream_schema.validate(http.get(self.url).text)
        if stream_url:
            headers = {"Referer": self.url}
            return HLSStream.parse_variant_playlist(self.session, stream_url, headers=headers)


__plugin__ = TVRPlus
