import unittest

from livecli import Livecli
from livecli.plugins.akamaihd import AkamaiHDPlugin
from livecli.stream import AkamaiHDStream


class TestPluginAkamaiHDPlugin(unittest.TestCase):
    def setUp(self):
        self.session = Livecli()

    def test_can_handle_url(self):
        should_match = [
            "akamaihd://https://example.com/index.mp3",
            "akamaihd://https://example.com/index.mp4",
        ]
        for url in should_match:
            self.assertTrue(AkamaiHDPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(AkamaiHDPlugin.can_handle_url(url))

    def _test_akamaihd(self, surl, url):
        plugin = self.session.resolve_url(surl)
        streams = plugin.streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, AkamaiHDStream))
        self.assertEqual(stream.url, url)

    def test_plugin_akamaihd(self):
        self._test_akamaihd("akamaihd://http://hostname.se/stream",
                            "http://hostname.se/stream")

        self._test_akamaihd("akamaihd://hostname.se/stream",
                            "http://hostname.se/stream")
