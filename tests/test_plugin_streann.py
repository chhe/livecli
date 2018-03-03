import unittest

from livecli.plugins.streann import Streann


class TestPluginStreann(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://ott.streann.com/streaming/player.html?EXAMPLE',
        ]
        for url in should_match:
            self.assertTrue(Streann.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Streann.can_handle_url(url))
