from io import BytesIO

from livecli import NoStreamsError
from livecli.plugins import Plugin
from livecli.options import Options
from livecli.stream import AkamaiHDStream
from livecli.stream import HLSStream
from livecli.stream import HTTPStream
from livecli.stream import RTMPStream
from livecli.stream import Stream


from livecli.plugin.api.support_plugin import testplugin_support


class TestStream(Stream):
    __shortname__ = "test"

    def open(self):
        return BytesIO(b'x' * 8192 * 2)


class TestPlugin(Plugin):
    options = Options({
        "a_option": "default"
    })

    @classmethod
    def can_handle_url(self, url):
        return "test.se" in url

    def _get_streams(self):
        if "empty" in self.url:
            return
        if "NoStreamsError" in self.url:
            raise NoStreamsError(self.url)

        streams = {}
        streams["test"] = TestStream(self.session)
        streams["rtmp"] = RTMPStream(self.session, dict(rtmp="rtmp://test.se"))
        streams["hls"] = HLSStream(self.session, "http://test.se/playlist.m3u8")
        streams["http"] = HTTPStream(self.session, "http://test.se/stream")
        streams["akamaihd"] = AkamaiHDStream(self.session, "http://test.se/stream")

        streams["240p"] = HTTPStream(self.session, "http://test.se/stream")
        streams["360p"] = HTTPStream(self.session, "http://test.se/stream")
        streams["1080p"] = HTTPStream(self.session, "http://test.se/stream")

        streams["350k"] = HTTPStream(self.session, "http://test.se/stream")
        streams["800k"] = HTTPStream(self.session, "http://test.se/stream")
        streams["1500k"] = HTTPStream(self.session, "http://test.se/stream")
        streams["3000k"] = HTTPStream(self.session, "http://test.se/stream")

        streams["480p"] = [HTTPStream(self.session, "http://test.se/stream"),
                           RTMPStream(self.session, dict(rtmp="rtmp://test.se"))]

        streams.update(testplugin_support._get_streams(self.session))

        return streams


__plugin__ = TestPlugin
