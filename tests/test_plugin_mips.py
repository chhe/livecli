import unittest

from livecli.plugins.mips import Mips


class TestPluginMips(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://mips.tv/example',
        ]
        for url in should_match:
            self.assertTrue(Mips.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Mips.can_handle_url(url))
