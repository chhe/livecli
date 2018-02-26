import unittest

from livecli.plugins.akamaihd import AkamaiHDPlugin


class TestPluginAkamaiHDPlugin(unittest.TestCase):
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
