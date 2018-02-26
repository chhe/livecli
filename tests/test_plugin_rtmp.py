import unittest

from livecli.plugins.rtmp import RTMPPlugin


class TestPluginRTMPPlugin(unittest.TestCase):
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
