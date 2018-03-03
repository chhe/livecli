import unittest

from livecli.plugins.tvcatchup import TVCatchup


class TestPluginTVCatchup(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://tvcatchup.com/watch/bbcone',
        ]
        for url in should_match:
            self.assertTrue(TVCatchup.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(TVCatchup.can_handle_url(url))
