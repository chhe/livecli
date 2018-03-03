import unittest

from livecli.plugins.skai import Skai


class TestPluginSkai(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.skai.gr/player/tvlive/',
        ]
        for url in should_match:
            self.assertTrue(Skai.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Skai.can_handle_url(url))
