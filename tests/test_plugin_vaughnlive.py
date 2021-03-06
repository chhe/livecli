import unittest

from livecli.plugins.vaughnlive import VaughnLive


class TestPluginVaughnLive(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://vaughnlive.tv/bluebirdnestboxcam',
        ]
        for url in should_match:
            self.assertTrue(VaughnLive.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(VaughnLive.can_handle_url(url))
