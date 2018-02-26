import unittest

from livecli.plugins.dailymotion import DailyMotion


class TestPluginDailyMotion(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "http://www.dailymotion.com/france24",
            "http://www.dailymotion.com/video/xigbvx",
            "http://www.dailymotion.com/video/x2j4lj9",
            "http://www.dailymotion.com/embed/video/x2j4lj9",
        ]
        for url in should_match:
            self.assertTrue(DailyMotion.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(DailyMotion.can_handle_url(url))
