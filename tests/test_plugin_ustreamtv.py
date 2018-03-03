import unittest

from livecli.plugins.ustreamtv import UStreamTV


class TestPluginUStreamTV(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.ustream.tv/channel/iss-hdev-payload',
        ]
        for url in should_match:
            self.assertTrue(UStreamTV.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(UStreamTV.can_handle_url(url))
