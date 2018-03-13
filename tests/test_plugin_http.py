import unittest

from livecli import Livecli
from livecli.plugins.http import HTTPStreamPlugin
from livecli.stream import HTTPStream


class TestPluginHTTPStreamPlugin(unittest.TestCase):

    def setUp(self):
        self.session = Livecli()

    def assertDictHas(self, a, b):
        for key, value in a.items():
            self.assertEqual(b[key], value)

    def test_can_handle_url(self):
        should_match = [
            "httpstream://https://example.com/index.mp3",
            "httpstream://https://example.com/index.mp4",
        ]
        for url in should_match:
            self.assertTrue(HTTPStreamPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(HTTPStreamPlugin.can_handle_url(url))

    def _test_http(self, surl, url, params):
        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, HTTPStream))
        self.assertEqual(stream.url, url)
        self.assertDictHas(params, stream.args)

    def test_plugin_http(self):
        self._test_http("httpstream://http://hostname.se/auth.php auth=('test','test2')",
                        "http://hostname.se/auth.php", dict(auth=("test", "test2")))

        self._test_http("httpstream://hostname.se/auth.php auth=('test','test2')",
                        "http://hostname.se/auth.php", dict(auth=("test", "test2")))

        self._test_http("httpstream://https://hostname.se/auth.php verify=False params={'key': 'a value'}",
                        "https://hostname.se/auth.php?key=a+value", dict(verify=False, params=dict(key='a value')))
