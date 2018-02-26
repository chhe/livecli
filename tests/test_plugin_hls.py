import unittest

from livecli.plugins.hls import HLSPlugin


class TestPluginHLSPlugin(unittest.TestCase):
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
