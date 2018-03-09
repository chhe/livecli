import unittest

from livecli.logger import Logger
from livecli.plugins.resolve import Resolve
from livecli.plugin.api.common import _iframe_re


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

        # Test 2 stream_base and whitelist_endswith playlists
        test_all_valid_2 = [
            "\/\/example.com/true1.mp4",
            "/true4_no_base/123.mp3",
            "//example.com/true5.m3u8",
            "http://example.com/master.gif",
            "http://example.com/master",
            "http://example.com/master.hls",
        ]

        stream_base = "http://example.com/base/stream/"
        test_list_2 = rr._make_url_list(test_all_valid_2, self_url, url_type="playlist", stream_base=stream_base)

        test_all_result_2 = [
            "https://example.com/true1.mp4",
            "http://example.com/base/stream/true4_no_base/123.mp3",
            "https://example.com/true5.m3u8",
            "http://example.com/master.hls",
        ]

        for test_url in test_all_result_2:
            self.assertIn(test_url, test_list_2)
        self.assertListEqual(sorted(test_all_result_2), sorted(test_list_2))

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

        res_test_list = [
            """
            <script type="text/javascript">
            window.location.href = 'https://www.youtube.com/embed/aqz-KE-bpKQ';
            </script>
            """,
        ]

        rr = Resolve("https://example.com")
        rr.manager = Logger()
        rr.logger = rr.manager.new_module("test")

        for test_res in res_test_list:
            m = rr._window_location(test_res)
            self.assertTrue(m)

        res_test_list_false = [
            """<!DOCTYPE html><html><body><h1>ABC</h1><p>123</p></body></html>
            """,
        ]

        rr = Resolve("https://example.com")
        rr.manager = Logger()
        rr.logger = rr.manager.new_module("test")

        for test_res in res_test_list_false:
            m = rr._window_location(test_res)
            self.assertFalse(m)

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
            m = _iframe_re.search(data)
            self.assertEqual(test_dict.get("result"), m.group("url"))

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

    def test_iframe_src(self):
        res_test_list = [
            """
            <iframe src="https://example.com/123.php" width="720" height="500" allowtransparency="true"/>
            """,
            """
            <div id="player">
                <script language='javascript'> document.write(unescape('%3Ciframe%20width%3D%22730%22%20height%3D%22440%22%20src%3D%22https%3A%2F%2Fwww.youtube.com%2Fembed%2Faqz-KE-bpKQ%3Fautoplay%3D1%22%20frameborder%3D%220%22%20gesture%3D%22media%22%20allow%3D%22encrypted-media%22%20allowfullscreen%3E%3C%2Fiframe%3E'));</script>
            </div>
            """,
        ]

        rr = Resolve("https://example.com")
        rr.manager = Logger()
        rr.logger = rr.manager.new_module("test")

        for test_res in res_test_list:
            m = rr._iframe_src(test_res)
            self.assertTrue(m)

        # test_iframe_src_false
        res_test_list_false = [
            """<!DOCTYPE html><html><body><h1>ABC</h1><p>123</p></body></html>
            """,
        ]

        for test_res in res_test_list_false:
            m = rr._iframe_src(test_res)
            self.assertFalse(m)

    def test_resolve_res(self):
        rr = Resolve("https://example.com")
        rr.manager = Logger()
        rr.logger = rr.manager.new_module("test")

        # Test for no items
        res_test_list_false = [
            """<!DOCTYPE html><html><body><h1>ABC</h1><p>123</p></body></html>
            """,
        ]

        for test_res in res_test_list_false:
            m = rr._resolve_res(test_res)
            self.assertFalse(m)
