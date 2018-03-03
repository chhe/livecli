import unittest

from livecli.plugins.nbcsports import NBCSports


class TestPluginNBCSports(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.nbcsports.com/video/example',
        ]
        for url in should_match:
            self.assertTrue(NBCSports.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(NBCSports.can_handle_url(url))
