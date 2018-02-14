import unittest

from livecli.logger import Logger
from livecli.plugins.resolve import Resolve


class TestPluginResolve(unittest.TestCase):
    def test_can_handle_url(self):
        # it should match everything
        self.assertTrue(Resolve.can_handle_url("resolve://local.local"))
        self.assertTrue(Resolve.can_handle_url("local.local"))

    def test_compare_url_path(self):
        rr = Resolve("https://example.com")
        from livecli.compat import urlparse

        blacklist_path = [
            ("expressen.se", "/_livetvpreview/"),
            ("facebook.com", "/plugins"),
            ("vesti.ru", "/native_widget.html"),
        ]

        url_true = "https://www.facebook.com/plugins/123.html"
        url_false = "https://example.com/123.html"

        parse_new_url = urlparse(url_true)
        self.assertTrue(rr.compare_url_path(parse_new_url, blacklist_path))

        parse_new_url = urlparse(url_false)
        self.assertFalse(rr.compare_url_path(parse_new_url, blacklist_path))

    def test_merge_path_list(self):
        rr = Resolve("https://example.com")
        blacklist_path = [
            ("expressen.se", "/_livetvpreview/"),
            ("facebook.com", "/plugins"),
            ("vesti.ru", "/native_widget.html"),
        ]

        blacklist_path_user = [
            "example.com/plugins",
            "example.com/myplugins",
        ]

        blacklist_path = rr.merge_path_list(blacklist_path, blacklist_path_user)

        blacklist_path_user_test = [
            ("example.com", "/plugins"),
            ("example.com", "/myplugins"),
        ]

        for test_url in blacklist_path_user_test:
            self.assertIn(test_url, blacklist_path)

    def test_make_url_list(self):
        self_url = "https://example.com"
        rr = Resolve(url=self_url)
        rr.manager = Logger()
        rr.logger = rr.manager.new_module("test")

        test_all_removed = [
            "http://about:blank",
            "http://expressen.se/_livetvpreview/123.html",
            "https://127.0.0.1",
            "https://adfox.ru",
            "https://example.com",
            "https://facebook.com/plugins123",
            "https://googletagmanager.com",
            "https://javascript:false",
            "https://vesti.ru/native_widget.html",
            "https://example.com/test"
            "https://example.com/test.gif",
            "https://example.com/test.jpg",
            "https://example.com/test.png",
            "https://example.com/test.svg",
            "https://example.com/test.vtt",
            "https://example.com/test/chat.html",
            "https://example.com/test/chat",
            "https://example.com/ad.php",
            "https://example.com/ad20.php",
            "https://example.com/ad5.php",
            "https://example.com/ads.htm",
            "https://example.com/ads.html",
            "https://example.com/ads/ads300x250.php",
            "https://example.com/ads468x60.htm",
            "https://example.com/ads468x60.html",
            "https://example.com/static/ads.htm",
            "https://example.com/static/ads.html",
            "https://example.com/static/ads/300x250_1217n.htm",
            "https://example.com/static/ads/300x250_1217n.html"
            "https://example.com/static/ads/468x60.htm",
            "https://example.com/static/ads/468x60.html",
            "https://example.com/static/ads468x60.htm",
            "https://example.com/static/ads468x60.html",
        ]

        test_all_valid = [
            "\/\/example.com/true1",
            "http&#58;//example.com/true2",
            "https&#58;//example.com/true3",
            "/true4_no_base/123.html",
            "//example.com/true5",
            "//example.com/true6",
            "//example.com/true6",
            "https://example.com/true7",
            "https://example.com/true7",
            "https://example.com/true7",
        ]
        test_all = test_all_removed + test_all_valid
        test_list = rr._make_url_list(test_all, self_url, url_type="iframe")

        test_all_result = [
            "https://example.com/true1",
            "http://example.com/true2",
            "https://example.com/true3",
            "https://example.com/true4_no_base/123.html",
            "https://example.com/true5",
            "https://example.com/true6",
            "https://example.com/true7",
        ]

        for test_url in test_all_result:
            self.assertIn(test_url, test_list)
        self.assertListEqual(sorted(test_all_result), sorted(test_list))

        # Test 2 stream_base
        test_all_valid_2 = [
            "\/\/example.com/true1",
            "/true4_no_base/123.html",
            "//example.com/true5",
        ]

        stream_base = "http://example.com/base/stream/"
        test_list_2 = rr._make_url_list(test_all_valid_2, self_url, url_type="playlist", stream_base=stream_base)

        test_all_result_2 = [
            "https://example.com/true1",
            "http://example.com/base/stream/true4_no_base/123.html",
            "https://example.com/true5",
        ]

        for test_url in test_all_result_2:
            self.assertIn(test_url, test_list_2)
        self.assertListEqual(sorted(test_all_result_2), sorted(test_list_2))

    def test_iframe_regex(self):
        regex_test_list = [
            {
                "data": """<iframe frameborder="0" src="http://local.local" width="650">iframe</iframe>""",
                "result": "http://local.local"
            },
            {
                "data": """<iframe src="http://local.local">    </iframe>""",
                "result": "http://local.local"
            },
            {
                "data": """<iframe src="http://local.local" width="800px"></iframe>""",
                "result": "http://local.local"
            },
            {
                "data": """<iframe height="600px" src="http://local.local"></iframe>""",
                "result": "http://local.local"
            },
            {
                "data": """<iframe height='600px' src='http://local.local'></iframe>""",
                "result": "http://local.local"
            },
            {
                "data": """</div>
                        <script type="text/javascript">_satellite.pageBottom();</script>
                        <iframe style="height:0px;width:0px;visibility:hidden" src="https://example.com/">
                            this frame prevents back forward cache
                            </iframe>
                        </body>""",
                "result": "https://example.com/"
            },
            {
                "data": """
                        <iframe src="https://example.com/123.php" width="720" height="500" allowtransparency="true"/>
                        """,
                "result": "https://example.com/123.php"
            },
            {
                "data": """
                        <script>
                            document.write('<ifr' + 'ame id="video" src="https://example.com/123.php" height="500" ></ifr' + 'ame>');
                        </script>
                        """,
                "result": "https://example.com/123.php"
            },
            {
                "data": """
                        <script>
                            document.write('<ifr'+'ame id="video" src="https://example.com/123.php" height="500" ></ifr'+'ame>');
                        </script>
                        """,
                "result": "https://example.com/123.php"
            },
            {
                "data": """
                        <iframe src="https://player.twitch.tv/?channel=monstercat" frameborder="0" allowfullscreen="true" scrolling="no" height="378" width="620"></iframe>
                        """,
                "result": "https://player.twitch.tv/?channel=monstercat"
            },
            {
                "data": """
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/aqz-KE-bpKQ" frameborder="0" gesture="media" allow="encrypted-media" allowfullscreen></iframe>
                        """,
                "result": "https://www.youtube.com/embed/aqz-KE-bpKQ"
            },
            {
                "data": """
                        <iframe frameborder="0" width="480" height="270" src="//www.dailymotion.com/embed/video/xigbvx" allowfullscreen></iframe>
                        """,
                "result": "//www.dailymotion.com/embed/video/xigbvx"
            },
            {
                "data": """
                        <iframe src="https://player.vgtrk.com/iframe/live/id/2961/showZoomBtn/false/isPlay/true/" scrolling="No" border="0" frameborder="0" width="660" height="494" mozallowfullscreen webkitallowfullscreen allowfullscreen></iframe>
                        """,
                "result": "https://player.vgtrk.com/iframe/live/id/2961/showZoomBtn/false/isPlay/true/"
            },
            {
                "data": """
                        <iframe SRC="/web/playeriframe.jsp"  frameborder="0" WIDTH=500 HEIGHT=400></iframe>
                        """,
                "result": "/web/playeriframe.jsp"
            },
            {
                "data": """
                        <iframe width="470" height="270" src="http&#58;//example.example/live/ABC123ABC" frameborder="0"></iframe>
                        """,
                "result": "http&#58;//example.example/live/ABC123ABC"
            },
            {
                "data": """
                    <iframe     id="random"
                        name="iframe"
                        src="https://example.com/dotall/iframe"
                        width="100%"
                        height="500"
                        scrolling="auto"
                        frameborder="1"
                        class="wrapper">
                        </iframe>
                    </div></div></div>
                    """,
                "result": "https://example.com/dotall/iframe",
            },
        ]
        rr = Resolve("https://example.com")
        for test_dict in regex_test_list:
            m = rr._iframe_re.search(test_dict.get("data"))
            self.assertIsNotNone(m)
            self.assertEqual(test_dict.get("result"), m.group("url"))

    def test_regex_iframe_false(self):
        rr = Resolve("https://example.com")
        regex_test_list = [
            """<iframe id="iframe" title="" frameborder="0" width="0" height="0" src=""></iframe>""",
            """<iframe name="g_iFrame1" width="70" src="logo"></iframe>""",
        ]
        if not hasattr(self, 'assertNotRegex'):
            self.assertNotRegex = self.assertNotRegexpMatches

        for data in regex_test_list:
            self.assertNotRegex(data, rr._iframe_re)

    def test_window_location(self):
        regex_test_list = [
            {
                "data": """
                    <script type="text/javascript">
                    window.location.href = 'https://www.youtube.com/embed/aqz-KE-bpKQ';
                    </script>
                        """,
                "result": "https://www.youtube.com/embed/aqz-KE-bpKQ"
            },
            {
                "data": """
                    <script type="text/javascript">
                    window.location.href = "https://www.youtube.com/watch?v=aqz-KE-bpKQ";
                    </script>
                        """,
                "result": "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
            },
        ]
        for test_dict in regex_test_list:
            rr = Resolve("https://example.com")
            m = rr._window_location_re.search(test_dict.get("data"))
            self.assertIsNotNone(m)
            self.assertEqual(test_dict.get("result"), m.group("url"))

    def test_unescape_iframe_re(self):
        from livecli.compat import unquote

        regex_test_list = [
            {
                "data": """
                        <div id="player">
                            <script language='javascript'> document.write(unescape('%3Ciframe%20width%3D%22730%22%20height%3D%22440%22%20src%3D%22https%3A%2F%2Fwww.youtube.com%2Fembed%2Faqz-KE-bpKQ%3Fautoplay%3D1%22%20frameborder%3D%220%22%20gesture%3D%22media%22%20allow%3D%22encrypted-media%22%20allowfullscreen%3E%3C%2Fiframe%3E'));</script>
                        </div>
                        """,
                "result": "https://www.youtube.com/embed/aqz-KE-bpKQ?autoplay=1"
            },
            {
                "data": """
                        <div id="player">
                            <script language='javascript'> document.write(unescape('%3C%69%66%72%61%6d%65%20width%3D%22730%22%20height%3D%22440%22%20src%3D%22https%3A%2F%2Fwww.youtube.com%2Fembed%2Faqz-KE-bpKQ%3Fautoplay%3D1%22%20frameborder%3D%220%22%20gesture%3D%22media%22%20allow%3D%22encrypted-media%22%20allowfullscreen%3E%3C%2Fiframe%3E'));</script>
                        </div>
                        """,
                "result": "https://www.youtube.com/embed/aqz-KE-bpKQ?autoplay=1"
            },
        ]
        rr = Resolve("https://example.com")
        for test_dict in regex_test_list:
            m = rr._unescape_iframe_re.search(test_dict.get("data"))
            self.assertIsNotNone(m)
            data = unquote(m.group("data"))
            self.assertIsNotNone(m)
            m = rr._iframe_re.search(data)
            self.assertEqual(test_dict.get("result"), m.group("url"))

    def test_regex_playlist_re(self):
        regex_test_list = [
            {
                "data": """<player frameborder="0" src="http://local.m3u8">""",
                "result": "http://local.m3u8"
            },
            {
                "data": """<player frameborder="0" src="http://local.m3u8?local">""",
                "result": "http://local.m3u8?local"
            },
            {
                "data": """<player frameborder="0" src="//local.m3u8?local">""",
                "result": "//local.m3u8?local"
            },
            {
                "data": """
                        file: "http://example.com:8081/edge/playlist.m3u8?wmsAuthSign=c9JnZbWludXR4",
                        """,
                "result": "http://example.com:8081/edge/playlist.m3u8?wmsAuthSign=c9JnZbWludXR4"
            },
            {
                "data": """
                        "hlsLivestreamURL": "https:\/\/live-http.example.com\/live\/_definst_\/mp4:123\/playlist.m3u8",
                        "appnameLive": "live",
                        "streaming": "true",
                        "autostart": "true",
                        """,
                "result": "https:\/\/live-http.example.com\/live\/_definst_\/mp4:123\/playlist.m3u8"
            },
            {
                "data": """
                        var player = new Clappr.Player({source: '/tv/tv.m3u8', mimeType: 'application/x-mpegURL'
                        """,
                "result": "/tv/tv.m3u8"
            },
            {
                "data": """
                        <player frameborder="0" src="local.m3u8?local">
                        """,
                "result": "local.m3u8?local"
            },
            {
                "data": """<player frameborder="0" src="http://local.f4m">""",
                "result": "http://local.f4m"
            },
            {
                "data": """<player frameborder="0" src="http://local.f4m?local">""",
                "result": "http://local.f4m?local"
            },
            {
                "data": """<player frameborder="0" src="//local.f4m?local">""",
                "result": "//local.f4m?local"
            },
            {
                "data": """<video src="http://local.mp3">""",
                "result": "http://local.mp3"
            },
            {
                "data": """<video src="http://local.mp4">""",
                "result": "http://local.mp4"
            },
            {
                "data": """<video src="//example.com/local.mp4">""",
                "result": "//example.com/local.mp4"
            },
            {
                "data": """
                        <video id='player_el' src='//example.com/video.mp4' width='100%' height='100%'
                        """,
                "result": "//example.com/video.mp4"
            },
            {
                "data": """
                        document.write( "<video src=http://999.999.999.999/live/playlist.m3u8?at=123 autoplay png> </video>");
                        """,
                "result": "http://999.999.999.999/live/playlist.m3u8?at=123"
            },
            {
                "data": """
                        document.write( "<video src=http://999.999.999.999/live/playlist.m3u8?at=123> </video>");
                        """,
                "result": "http://999.999.999.999/live/playlist.m3u8?at=123"
            },
            {
                "data": """
                        \&quot;hlsMasterPlaylistUrl\&quot;:\&quot;https://example.com/hls/video.m3u8?p\&quot;,
                        """,
                "result": "https://example.com/hls/video.m3u8?p"
            },
        ]
        for test_dict in regex_test_list:
            rr = Resolve("https://example.com")
            m = rr._playlist_re.search(test_dict.get("data"))
            self.assertIsNotNone(m)
            self.assertEqual(test_dict.get("result"), m.group("url"))

    def test_regex_playlist_re_false(self):
        regex_test_list = [
            """<player frameborder="0" src="local.apk?local">""",
            """<player frameborder="0" src="http://local.mpk">""",
            """meta title="broken_title_url.mp4">""",
            """video">broken_title_url22.mp4</span></div><div style="float""",
            """video">broken_title_url22.mp4"float""",
            """if(options.livestream==true){
                 PlayerSetup.source.hls=options.m3u8;
               }
            """,
            """getCurrentVideoSrc: function(){
                 return $("#player").data("player").mp4;
               },
            """,
        ]
        if not hasattr(self, 'assertNotRegex'):
            self.assertNotRegex = self.assertNotRegexpMatches

        for data in regex_test_list:
            rr = Resolve("https://example.com")
            self.assertNotRegex(data, rr._playlist_re)

    def test_regex_ads_path(self):
        regex_test_list = [
            "/ad.php",
            "/ad20.php",
            "/ad5.php",
            "/ads.htm",
            "/ads.html",
            "/ads/ads300x250.php",
            "/ads468x60.htm",
            "/ads468x60.html",
            "/static/ads.htm",
            "/static/ads.html",
            "/static/ads/300x250_1217n.htm",
            "/static/ads/300x250_1217n.html"
            "/static/ads/468x60.htm",
            "/static/ads/468x60.html",
            "/static/ads468x60.htm",
            "/static/ads468x60.html",
        ]
        for test_url in regex_test_list:
            rr = Resolve("https://example.com")
            m = rr._ads_path.match(test_url)
            self.assertIsNotNone(m)
