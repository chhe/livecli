import unittest

from livecli.plugins.gardenersworld import GardenersWorld


class TestPluginGardenersWorld(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.gardenersworld.com/how-to',
        ]
        for url in should_match:
            self.assertTrue(GardenersWorld.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(GardenersWorld.can_handle_url(url))
