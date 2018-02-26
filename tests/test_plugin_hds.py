import unittest

from livecli.plugins.hds import HDSPlugin


class TestPluginHDSPlugin(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "hds://https://example.com/index.hds",
            "https://example.com/index.f4m?test=true",
            "https://example.com/index.f4m",
        ]
        for url in should_match:
            self.assertTrue(HDSPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(HDSPlugin.can_handle_url(url))
