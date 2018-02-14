import re

from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.plugin.api import useragents
from livecli.plugin.api import validate
from livecli.stream import HDSStream
from livecli.stream import HLSStream
from livecli.stream import HTTPStream

__livecli_docs__ = {
    "domains": [
        "tv.aftonbladet.se",
    ],
    "geo_blocked": [],
    "notes": "",
    "live": True,
    "vod": True,
    "last_update": "2018-02-14",
}


class Aftonbladet(Plugin):
    """Plugin for swedish news paper Aftonbladet's streaming service."""

    _url_re = re.compile(r"https?://tv\.aftonbladet\.se/[^/]+/[^/]+/(?P<id>\d+)")

    api_url = "https://svp.vg.no/svp/api/v1/ab/assets/{0}?appName=svp-player"

    _video_schema = validate.Schema(
        {
            validate.optional("title"): validate.text,
            validate.optional("assetType"): validate.text,
            validate.optional("streamType"): validate.text,
            validate.optional("status"): validate.text,
            "streamUrls": {
                validate.optional("hls"): validate.any(validate.text, None),
                validate.optional("hds"): validate.any(validate.text, None),
                validate.optional("mp4"): validate.any(validate.text, None),
            },
        }
    )

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):
        m_url = self._url_re.match(self.url)
        if not m_url:
            return

        video_id = m_url.group("id")

        headers = {
            "User-Agent": useragents.FIREFOX,
            "Referer": self.url
        }

        res = http.get(self.api_url.format(video_id), headers=headers)
        data = http.json(res, schema=self._video_schema)

        title = data.get("title")
        streamurls = data.get("streamUrls")

        if title:
            self.stream_title = title

        if streamurls:
            hls_url = streamurls.get("hls")
            if hls_url:
                streams = HLSStream.parse_variant_playlist(self.session, hls_url, headers=headers).items()
                if not streams:
                    yield "live", HLSStream(self.session, hls_url, headers=headers)
                for s in streams:
                    yield s

            hds_url = streamurls.get("hds")
            if hds_url:
                for s in HDSStream.parse_manifest(self.session, hds_url, headers=headers).items():
                    yield s

            mp4_url = streamurls.get("mp4")
            if mp4_url:
                name = "live"
                yield name, HTTPStream(self.session, mp4_url, headers=headers)


__plugin__ = Aftonbladet
