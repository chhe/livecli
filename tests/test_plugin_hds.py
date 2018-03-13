import requests_mock
import unittest

from livecli import Livecli
from livecli.logger import Logger
from livecli.plugin.plugin import LOW_PRIORITY
from livecli.plugin.plugin import NO_PRIORITY
from livecli.plugin.plugin import NORMAL_PRIORITY
from livecli.plugins.hds import HDSPlugin
from livecli.stream import HDSStream

text_manifest = """<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="http://ns.adobe.com/f4m/1.0">
    <streamType>recorded</streamType>
    <baseURL>http://mocked/hds/</baseURL>
    <duration>269.293</duration>
    <bootstrapInfo profile="named" id="bootstrap_1">AAAAm2Fic3QAAAAAAAAAAQAAAAPoAAAAAAAEG+0AAAAAAAAAAAAAAAAAAQAAABlhc3J0AAAAAAAAAAABAAAAAQAAAC4BAAAAVmFmcnQAAAAAAAAD6AAAAAAEAAAAAQAAAAAAAAAAAAAXcAAAAC0AAAAAAAQHQAAAE5UAAAAuAAAAAAAEGtUAAAEYAAAAAAAAAAAAAAAAAAAAAAA=</bootstrapInfo>
    <media url="index" bootstrapInfoId="bootstrap_1" bitrate="2148" width="1280" height="720" videoCodec="avc1.4d401f" audioCodec="mp4a.40.2">
        <metadata></metadata>
    </media>
</manifest>"""


class TestPluginHDSPlugin(unittest.TestCase):
    def setUp(self):
        self.session = Livecli()
        self.manager = Logger()
        self.logger = self.manager.new_module("test")

    def test_can_handle_url(self):
        should_match = [
            "hds://https://example.com/index.hds",
            "https://example.com/index.f4m?test=true",
            "https://example.com/index.f4m",
        ]
        for url in should_match:
            self.assertTrue(HDSPlugin.can_handle_url(url))

        should_not_match = [
            "https://example.com/index.html",
        ]
        for url in should_not_match:
            self.assertFalse(HDSPlugin.can_handle_url(url))

    def test_priority(self):
        test_data = [
            ("https://example.com/index.f4m", LOW_PRIORITY),
            ("hds://https://example.com/index.f4m", NORMAL_PRIORITY),
            ("https://example.com/index.html", NO_PRIORITY),
        ]
        for url, status in test_data:
            self.assertEqual(HDSPlugin.priority(url), status)

    def test_get_streams(self):
        HDSPlugin.bind(self.session, "test.plugin.hds")

        url_manifest = "https://mocked/manifest.f4m"

        with requests_mock.Mocker() as mock:
            mock.get(url_manifest, text=text_manifest)

            plugin = HDSPlugin(url_manifest)
            streams = plugin._get_streams()

            self.assertIn("720p", streams)

            stream = streams["720p"]
            self.assertTrue(isinstance(stream, HDSStream))
            self.assertEqual(stream.url, "index")
