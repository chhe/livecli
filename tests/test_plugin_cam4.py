import unittest

from livecli.plugins.cam4 import Cam4


class TestPluginCam4(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://cam4.com/example',
            'https://fr.cam4.com/example',
            'https://nl.cam4.com/example',
            'https://pl.cam4.com/example',
            'https://www.cam4.com/example',
        ]
        for url in should_match:
            self.assertTrue(Cam4.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Cam4.can_handle_url(url))
