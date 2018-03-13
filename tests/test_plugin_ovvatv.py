import requests_mock
import unittest

from livecli import Livecli
from livecli.logger import Logger
from livecli.plugin import api
from livecli.plugins.ovvatv import ovvaTV

try:
    from unittest.mock import patch
except ImportError:
    # python 2.7
    from mock import patch

text_master_hls = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1152000
index.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=640000
index.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=320000
index.m3u8
"""

text_hls = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:3080235
#EXT-X-TARGETDURATION:2
#EXTINF:2.000,
3080235.ts
"""


class TestPluginovvaTV(unittest.TestCase):

    def setUp(self):
        self.session = Livecli()
        self.manager = Logger()
        self.logger = self.manager.new_module("test")

    def test_can_handle_url(self):
        should_match = [
            'https://1plus1.video/tvguide/embed/1?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/16?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/2?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/3?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/4?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/5?autoplay=1&l=ua',
            'https://1plus1.video/tvguide/embed/7?autoplay=1&l=ua',
        ]
        for url in should_match:
            self.assertTrue(ovvaTV.can_handle_url(url))

        should_not_match = [
            'https://1plus1.video/',
            'https://1plus1.video/tvguide/1plus1/online',
            'https://1plus1.video/tvguide/1plus1in/online',
            'https://1plus1.video/tvguide/2plus2/online',
            'https://1plus1.video/tvguide/tet/online',
            'https://1plus1.video/tvguide/plusplus/online',
            'https://1plus1.video/tvguide/bigudi/online',
            'https://1plus1.video/tvguide/uniantv/online',
        ]
        for url in should_not_match:
            self.assertFalse(ovvaTV.can_handle_url(url))

    @patch("livecli.plugins.ovvatv.http")
    def test_get_streams(self, mock_http):
        mock_http.get = api.HTTPSession().get

        text_website_false = "<html></html>"
        text_date = """<div class="o-message-timer" data-timer="1520979240" data-titles=""></div>"""
        text_website = """
        <div id="ovva-player">
        </div>
        <script type="text/javascript">window.onload=function(){ new OVVA("ovva-player","%s")};</script>
        </body>"""

        data = "eyJpZCI6IjE0IiwiYmFsYW5jZXIiOiJodHRwczpcL1wvZ3JhbmRjZW50cmFsLm92dmEudHZcL2xiXC9saXZlXC8xMjNcLzEyM1wvIn0="
        data_e = "dGVzdA=="

        text_302 = """302=http://mocked/ua/master.m3u8"""

        ovvaTV.bind(self.session, "test.plugin.ovvatv")

        self_url = "https://1plus1.video/tvguide/embed/1?autoplay=1&l=ua"
        self_url_date = "https://1plus1.video/tvguide/embed/20?autoplay=1&l=ua"
        self_url_error = "https://1plus1.video/tvguide/embed/33?autoplay=1&l=ua"
        self_url_false = "https://1plus1.video/tvguide/embed/11?autoplay=1&l=ua"

        url_302 = "https://grandcentral.ovva.tv/lb/live/123/123/"
        url_m3u8 = "http://mocked/ua/index.m3u8"
        url_master_m3u8 = "http://mocked/ua/master.m3u8"

        with requests_mock.Mocker() as mock:
            mock.get(self_url_date, text=text_date)
            mock.get(self_url_error, text=text_website % data_e)
            mock.get(self_url_false, text=text_website_false)
            mock.get(self_url, text=text_website % data)

            mock.get(url_302, text=text_302)
            mock.get(url_m3u8, text=text_hls)
            mock.get(url_master_m3u8, text=text_master_hls)

            plugin = ovvaTV(self_url)
            streams = plugin._get_streams()
            self.assertIn("640k", streams)

            # False tests
            for url in [self_url_false, self_url_date]:
                plugin_false = ovvaTV(url)
                streams_false = plugin_false._get_streams()

                self.assertIsNone(streams_false)
