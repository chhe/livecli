from __future__ import print_function
import re

from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.plugin.api import validate
from livecli.stream import RTMPStream
from livecli.plugins.common_jwplayer import _js_to_json
from livecli.utils import parse_json


class Sportal(Plugin):
    swf_url = "http://img2.sportal.bg/images/svp/videoplayer.swf"
    url_re = re.compile(r"https?://(?:www\.)?sportal\.bg/sportal_live_tv.php.*")
    _playlist_re = re.compile(r"\(\{.*playlist: (\[.*\]),.*?\}\);", re.DOTALL)
    _playlist_schema = validate.Schema(
        validate.transform(_playlist_re.search),
        validate.any(
            None,
            validate.all(
                validate.get(1),
                validate.transform(_js_to_json),
                validate.transform(parse_json),
                [{
                    "streamer": validate.url(scheme="rtmp"),
                    "levels": [
                        {"bitrate": int, "file": validate.text}
                    ]
                }],
                validate.get(0)
            )
        )
    )

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        res = http.get(self.url)

        playlist = self._playlist_schema.validate(res.text)
        if playlist:
            for level in playlist["levels"]:
                q = "{0}k".format(level["bitrate"])
                s = RTMPStream(self.session,
                               redirect=True,
                               params={"rtmp": playlist["streamer"],
                                       "playpath": level["file"],
                                       "pageUrl": self.url,
                                       "z": True,
                                       "swfUrl": self.swf_url})
                yield q, s


__plugin__ = Sportal
