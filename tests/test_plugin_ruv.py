import unittest

from livecli.plugins.ruv import Ruv


class TestPluginRuv(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "https://www.ruv.is/ras-1",
            "https://www.ruv.is/ras-2",
            "https://www.ruv.is/ras1",
            "https://www.ruv.is/ras2",
            "https://www.ruv.is/rondo",
            "https://www.ruv.is/ruv",
            "https://www.ruv.is/ruv2",
            "https://www.ruv.is/ruv-2/",
        ]
        for url in should_match:
            self.assertTrue(Ruv.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(Ruv.can_handle_url(url))
