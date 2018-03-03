import unittest

from livecli.plugins.smashcast import Smashcast


class TestPluginSmashcast(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.smashcast.tv/jurnalfm',
        ]
        for url in should_match:
            self.assertTrue(Smashcast.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Smashcast.can_handle_url(url))
