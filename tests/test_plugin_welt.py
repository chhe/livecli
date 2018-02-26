import unittest

from livecli.plugins.welt import Welt


class TestPluginWelt(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "https://www.welt.de/mediathek/dokumentation/natur-und-wildlife/animal-fight-club/sendung157940043/Animal-Fight-Club-Monster-Chaos.html",
            "https://www.welt.de/tv-programm-live-stream/",
        ]
        for url in should_match:
            self.assertTrue(Welt.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(Welt.can_handle_url(url))
