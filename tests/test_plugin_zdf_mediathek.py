import unittest

from livecli.plugins.zdf_mediathek import zdf_mediathek


class TestPluginzdf_mediathek(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "https://www.zdf.de/nachrichten/heute-sendungen/180222-h17-gesamtsendung-100.html",
            "https://www.zdf.de/sender/zdf/zdf-live-beitrag-100.html",
        ]
        for url in should_match:
            self.assertTrue(zdf_mediathek.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(zdf_mediathek.can_handle_url(url))
