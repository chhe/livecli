import unittest

from livecli.plugins.younow import younow


class TestPluginyounow(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.younow.com/example',
        ]
        for url in should_match:
            self.assertTrue(younow.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(younow.can_handle_url(url))
