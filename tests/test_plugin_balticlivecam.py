import unittest

from livecli.plugins.balticlivecam import BalticLivecam


class TestPluginBalticLivecam(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "https://balticlivecam.com/cameras/russia/sochi/primorsky-beach/",
            "https://balticlivecam.com/cameras/russia/sochi/sochi-panorama/",
        ]
        for url in should_match:
            self.assertTrue(BalticLivecam.can_handle_url(url))

        should_not_match = [
            "http://www.example.com/",
        ]
        for url in should_not_match:
            self.assertFalse(BalticLivecam.can_handle_url(url))
