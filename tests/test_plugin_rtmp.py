import unittest

from livecli import Livecli
from livecli.plugins.rtmp import RTMPPlugin
from livecli.stream import RTMPStream


class TestPluginRTMPPlugin(unittest.TestCase):
    def setUp(self):
        self.session = Livecli()

    def assertDictHas(self, a, b):
        for key, value in a.items():
            self.assertEqual(b[key], value)

    def test_can_handle_url(self):
        should_match = [
            "rtmp://https://example.com/",
            "rtmpe://https://example.com/",
            "rtmps://https://example.com/",
            "rtmpt://https://example.com/",
            "rtmpte://https://example.com/",
        ]
        for url in should_match:
            self.assertTrue(RTMPPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(RTMPPlugin.can_handle_url(url))

    def _test_rtmp(self, surl, url, params):
        plugin = self.session.resolve_url(surl)
        streams = plugin.streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, RTMPStream))
        self.assertEqual(stream.params["rtmp"], url)
        self.assertDictHas(params, stream.params)

    def test_plugin_rtmp(self):
        self._test_rtmp("rtmp://hostname.se/stream",
                        "rtmp://hostname.se/stream", dict())

        self._test_rtmp("rtmp://hostname.se/stream live=1 qarg='a \\'string' noq=test",
                        "rtmp://hostname.se/stream", dict(live=True, qarg='a \'string', noq="test"))

        self._test_rtmp("rtmp://hostname.se/stream live=1 num=47",
                        "rtmp://hostname.se/stream", dict(live=True, num=47))

        self._test_rtmp("rtmp://hostname.se/stream conn=['B:1','S:authMe','O:1','NN:code:1.23','NS:flag:ok','O:0']",
                        "rtmp://hostname.se/stream",
                        dict(conn=['B:1', 'S:authMe', 'O:1', 'NN:code:1.23', 'NS:flag:ok', 'O:0']))
