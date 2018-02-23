import unittest

from livecli.plugins.twitch import Twitch


class TestPluginTwitch(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "https://www.twitch.tv/twitch",
            "https://www.twitch.tv/videos/150942279",
            "https://clips.twitch.tv/ObservantBenevolentCarabeefPhilosoraptor",
        ]
        for url in should_match:
            self.assertTrue(Twitch.can_handle_url(url))

        should_not_match = [
            "https://www.twitch.tv",
        ]
        for url in should_not_match:
            self.assertFalse(Twitch.can_handle_url(url))
