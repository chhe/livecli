import unittest

from livecli.plugins.atresplayer import AtresPlayer


class TestPluginAtresPlayer(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            "http://www.atresplayer.com/directos/television/antena3/",
            "http://www.atresplayer.com/directos/television/lasexta/"
        ]
        for url in should_match:
            self.assertTrue(AtresPlayer.can_handle_url(url))

        should_not_match = [
            "http://www.atresplayer.com/",
        ]
        for url in should_not_match:
            self.assertFalse(AtresPlayer.can_handle_url(url))
