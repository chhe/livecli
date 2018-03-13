import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from livecli import Livecli
from livecli.plugin.plugin import LOW_PRIORITY
from livecli.plugin.plugin import NO_PRIORITY
from livecli.plugin.plugin import NORMAL_PRIORITY
from livecli.plugins.hls import HLSPlugin
from livecli.stream import HLSStream


class TestPluginHLSPlugin(unittest.TestCase):
    def setUp(self):
        self.session = Livecli()

    def test_can_handle_url(self):
        should_match = [
            "https://example.com/index.m3u8",
            "https://example.com/index.m3u8?test=true",
            "hls://https://example.com/index.m3u8",
            "hlsvariant://https://example.com/index.m3u8",
        ]
        for url in should_match:
            self.assertTrue(HLSPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(HLSPlugin.can_handle_url(url))

    def test_priority(self):
        test_data = [
            ("https://example.com/index.m3u8", LOW_PRIORITY),
            ("hls://https://example.com/index.m3u8", NORMAL_PRIORITY),
            ("https://example.com/index.html", NO_PRIORITY),
        ]
        for url, status in test_data:
            self.assertEqual(HLSPlugin.priority(url), status)

    @patch('livecli.stream.HLSStream.parse_variant_playlist')
    def _test_hls(self, surl, url, mock_parse):
        mock_parse.return_value = {}

        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        self.assertTrue("live" in streams)
        mock_parse.assert_called_with(self.session, url)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, HLSStream))
        self.assertEqual(stream.url, url)

    @patch('livecli.stream.HLSStream.parse_variant_playlist')
    def _test_hlsvariant(self, surl, url, mock_parse):
        mock_parse.return_value = {"best": HLSStream(self.session, url)}

        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        mock_parse.assert_called_with(self.session, url)

        self.assertFalse("live" in streams)
        self.assertTrue("best" in streams)

        stream = streams["best"]
        self.assertTrue(isinstance(stream, HLSStream))
        self.assertEqual(stream.url, url)

    def test_plugin_hls(self):
        self._test_hls("hls://https://hostname.se/playlist.m3u8",
                       "https://hostname.se/playlist.m3u8")

        self._test_hls("hls://hostname.se/playlist.m3u8",
                       "http://hostname.se/playlist.m3u8")

        self._test_hlsvariant("hls://hostname.se/playlist.m3u8",
                              "http://hostname.se/playlist.m3u8")

        self._test_hlsvariant("hls://https://hostname.se/playlist.m3u8",
                              "https://hostname.se/playlist.m3u8")
