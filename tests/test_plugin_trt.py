import unittest

from livecli.plugins.trt import TRT


class TestPluginTRT(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            'http://www.trt.net.tr/anasayfa/canli.aspx?y=tv&k=trt1',
        ]
        for url in should_match:
            self.assertTrue(TRT.can_handle_url(url))

        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse(TRT.can_handle_url(url))
