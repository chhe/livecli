import unittest

from livecli.plugins.tga import Tga


class TestPluginTga(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://star.longzhu.com/lpl',
        ]
        for url in should_match:
            self.assertTrue(Tga.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Tga.can_handle_url(url))
