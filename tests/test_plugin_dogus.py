import unittest

from livecli.plugins.dogus import Dogus


class TestPluginDogus(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.ntvspor.net/canli-yayin',
            'http://eurostartv.com.tr/canli-izle',
        ]
        for url in should_match:
            self.assertTrue(Dogus.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(Dogus.can_handle_url(url))
