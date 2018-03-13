import requests_mock
import unittest

from livecli.plugin import api
from livecli import Livecli
from livecli.logger import Logger
from livecli.plugins.inter import Inter

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


class TestPluginInter(unittest.TestCase):

    def setUp(self):
        self.session = Livecli()
        self.manager = Logger()
        self.logger = self.manager.new_module("test")

    def test_can_handle_url(self):
        should_match = [
            "http://inter.ua/ru/live",
            "http://www.k1.ua/uk/live",
            "http://ntn.ua/ru/live",
        ]
        for url in should_match:
            self.assertTrue(Inter.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(Inter.can_handle_url(url))

    @patch("livecli.plugins.inter.http")
    def test_get_streams(self, mock_http):
        mock_http.get = api.HTTPSession().get
        mock_http.json = api.HTTPSession().json

        text_website_false = "<html></html>"
        text_website = """
            <script>
              (function () {
                  function initPlayer() {
                      window.VideePlayer.initPlayers([{
                          el: placementEL,
                          config: {
                              autoplay: true,
                              VMAPTag: "URL",
                              size: '354x628',
                              adControls: ['progress', 'volume', 'skip'],
                              adRoll: {
                                  pause: [
                                      {
                                        vastAdTagUrl: 'URL'
                                      }
                                  ]
                              },
                              HLSSource: '%s'
                          },
                          id: 123456
                      }]);
                  }
              })();
            </script>"""

        text_HLSSource = """
            {"redir":"http://mocked/inter/ua/index.m3u8"}
            """

        Inter.bind(self.session, "test.plugin.inter")

        self_url = "http://mocked/inter/ua/live"
        self_url_false = "http://mocked/inter/ua/live_false"
        url_HLSSource = "http://mocked/inter/ua/live/inters_json"
        url_m3u8 = "http://mocked/inter/ua/index.m3u8"
        url_master_m3u8 = "http://mocked/inter/ua/master.m3u8"

        with requests_mock.Mocker() as mock:
            mock.get(self_url_false, text=text_website_false)
            mock.get(url_HLSSource, text=text_HLSSource)
            mock.get(url_m3u8, text=text_hls)
            mock.get(url_master_m3u8, text=text_master_hls)

            # 1. test normal hls with redir
            # 2. test playlist hls without redir
            for _url, _name in [(url_HLSSource, "live"),
                                (url_master_m3u8, "640k")]:
                mock.get(self_url, text=text_website % _url)

                plugin = Inter(self_url)

                streams = plugin._get_streams()
                print(streams)
                self.assertIn(_name, streams)

            # _playlist_re is False test
            plugin_false = Inter(self_url_false)
            streams_false = plugin_false._get_streams()

            self.assertIsNone(streams_false)
