import unittest

from livecli.plugins.http import HTTPStreamPlugin


class TestPluginHTTPStreamPlugin(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "httpstream://https://example.com/index.mp3",
            "httpstream://https://example.com/index.mp4",
        ]
        for url in should_match:
            self.assertTrue(HTTPStreamPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(HTTPStreamPlugin.can_handle_url(url))
