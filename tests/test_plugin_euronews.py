import requests_mock
import unittest

from livecli.plugin import api
from livecli import Livecli
from livecli.logger import Logger
from livecli.plugins.euronews import Euronews

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


class TestPluginEuronews(unittest.TestCase):

    def setUp(self):
        self.session = Livecli()
        self.manager = Logger()
        self.logger = self.manager.new_module("test")

    def test_can_handle_url(self):
        # should match
        self.assertTrue(Euronews.can_handle_url("http://www.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://fr.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://de.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://it.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://es.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://pt.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://ru.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://ua.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://tr.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://gr.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://hu.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://fa.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://arabic.euronews.com/live"))
        self.assertTrue(Euronews.can_handle_url("http://www.euronews.com/2017/05/10/peugeot-expects-more-opel-losses-this-year"))
        self.assertTrue(Euronews.can_handle_url("http://fr.euronews.com/2017/05/10/l-ag-de-psa-approuve-le-rachat-d-opel"))

        # shouldn't match
        self.assertFalse(Euronews.can_handle_url("http://www.tvcatchup.com/"))
        self.assertFalse(Euronews.can_handle_url("http://www.youtube.com/"))

    @patch("livecli.plugins.euronews.http")
    def test_get_streams_live(self, mock_http):
        mock_http.get = api.HTTPSession().get
        mock_http.json = api.HTTPSession().json

        test_api_live_1 = """{"url":"http://mocked/eu/live/2.json"}"""
        test_api_live_2 = """{"status":"ok","protocol":"hls","primary":"http://mocked/eu/master.m3u8","backup":"http://mocked/eu/master.m3u8"}"""

        Euronews.bind(self.session, "test.plugin.inter")

        url_live = "http://www.euronews.com/live"
        url_api_live_1 = "http://www.euronews.com/api/watchlive.json"
        url_api_live_2 = "http://mocked/eu/live/2.json"
        url_m3u8 = "http://mocked/eu/index.m3u8"
        url_master_m3u8 = "http://mocked/eu/master.m3u8"

        with requests_mock.Mocker() as mock:
            mock.get(url_api_live_1, text=test_api_live_1)
            mock.get(url_api_live_2, text=test_api_live_2)
            mock.get(url_m3u8, text=text_hls)
            mock.get(url_master_m3u8, text=text_master_hls)

            for _url, _name in [(url_live, "1152k")]:

                plugin = Euronews(_url)
                streams = plugin._get_streams()
                self.assertIn(_name, streams)

    @patch("livecli.plugins.euronews.http")
    def test_get_streams_vod(self, mock_http):
        mock_http.get = api.HTTPSession().get
        mock_http.json = api.HTTPSession().json

        text_website_vod = """
            <meta property="article:section" content="news_business" />
            <meta property="og:video" content="https://video.euronews.com/mp4/EN/03_E.mp4" />
            <meta name="twitter:site" content="@euronews" />
            """

        Euronews.bind(self.session, "test.plugin.inter")

        url_vod = "http://www.euronews.com/2017/05/10/peugeot-expects-more-opel-losses-this-year"

        with requests_mock.Mocker() as mock:
            mock.get(url_vod, text=text_website_vod)

            for _url, _name in [(url_vod, "vod")]:

                plugin = Euronews(_url)

                streams = plugin._get_streams()
                self.assertIn(_name, streams)
