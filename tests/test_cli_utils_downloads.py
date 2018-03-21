import re
import unittest

from livecli_cli.utils.downloads import get_id_for_filename
from livecli_cli.utils.downloads import get_output_format
from livecli_cli.utils.downloads import get_url_re_from_module

from livecli.plugins.earthcam import EarthCam
from livecli.plugins.resolve import Resolve


class TestCliUtilsDownloads(unittest.TestCase):

    def test_get_id_for_filename(self):
        url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
        m = re.compile(r""".*v=(?P<video_id>.*)""").match(url)

        self.assertEqual(get_id_for_filename(m), "aqz-KE-bpKQ")

    def test_get_url_re_from_module(self):
        self.assertIsNotNone(get_url_re_from_module(EarthCam))
        self.assertIsNotNone(get_url_re_from_module(Resolve))

    def test_get_output_format(self):
        self.assertEqual(get_output_format("hds"), ".mp4")
        self.assertEqual(get_output_format("hls"), ".ts")
        self.assertEqual(get_output_format("rtmp"), ".flv")

        self.assertEqual(get_output_format("ERROR"), ".mp4")
