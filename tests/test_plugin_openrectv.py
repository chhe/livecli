import unittest

from livecli.plugins.openrectv import OPENRECtv


class TestPluginOPENRECtv(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'https://www.openrec.tv/live/DXRLAPSGTpx',
            'https://www.openrec.tv/movie/JsDw3rAV2Rj',
        ]
        for url in should_match:
            self.assertTrue(OPENRECtv.can_handle_url(url))

        should_not_match = [
            'https://www.openrec.tv/',
        ]
        for url in should_not_match:
            self.assertFalse(OPENRECtv.can_handle_url(url))
