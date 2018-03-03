import unittest

from livecli.plugins.ssh101 import SSH101


class TestPluginSSH101(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.ssh101.com/live/test',
        ]
        for url in should_match:
            self.assertTrue(SSH101.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(SSH101.can_handle_url(url))
