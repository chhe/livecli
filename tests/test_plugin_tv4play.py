import unittest

from livecli.plugins.tv4play import TV4Play


class TestPluginTV4Play(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            # 'https://www.fotbollskanalen.se/video/3959760/roma-tranaren-jag-skulle-vilja-trana-balotelli/',
            # 'https://www.tv4play.se/program/farmen/3957213',
            'https://www.fotbollskanalen.se/video/videoid=3959760',
            'https://www.tv4play.se/program/farmen/videoid=3957213',
        ]
        for url in should_match:
            self.assertTrue(TV4Play.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(TV4Play.can_handle_url(url))
