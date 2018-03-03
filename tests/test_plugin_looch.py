import unittest

from livecli.plugins.looch import Looch


class TestPluginLooch(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://looch.tv/EXAMPLE',
        ]
        for url in should_match:
            self.assertTrue(Looch.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Looch.can_handle_url(url))
