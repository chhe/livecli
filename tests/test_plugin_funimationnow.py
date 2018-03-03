import unittest

from livecli.plugins.funimationnow import FunimationNow


class TestPluginFunimationNow(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.funimation.com/',
            'https://www.funimationnow.uk/',
        ]
        for url in should_match:
            self.assertTrue(FunimationNow.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(FunimationNow.can_handle_url(url))
