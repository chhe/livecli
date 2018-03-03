import unittest

from livecli.plugins.nbc import NBC


class TestPluginNBC(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.nbc.com/example/video/example/123123',
        ]
        for url in should_match:
            self.assertTrue(NBC.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(NBC.can_handle_url(url))
