import unittest

from livecli.plugin.api.validate import xml_element, text
from livecli.utils import update_scheme

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from livecli import PluginError
from livecli.compat import parse_qsl
from livecli.compat import urlparse
from livecli.plugin.api import validate
from livecli.utils import absolute_url
from livecli.utils import filter_urlquery
from livecli.utils import hours_minutes_seconds
from livecli.utils import parse_json
from livecli.utils import parse_qsd
from livecli.utils import parse_xml
from livecli.utils import prepend_www
from livecli.utils import time_to_offset
from livecli.utils import verifyjson


class TestUtil(unittest.TestCase):
    def test_verifyjson(self):
        self.assertEqual(verifyjson({"test": 1}, "test"),
                         1)

        self.assertRaises(PluginError, verifyjson, None, "test")
        self.assertRaises(PluginError, verifyjson, {}, "test")

    def test_absolute_url(self):
        self.assertEqual("http://test.se/test",
                         absolute_url("http://test.se", "/test"))
        self.assertEqual("http://test2.se/test",
                         absolute_url("http://test.se", "http://test2.se/test"))

    def test_filter_urlquery(self):
        test_data = [
            {
                "url": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123&n=20&b=496,896,1296,1896",
                "keys": ["hdnea"],
                "keys_status": False,
                "result": "http://example.com/z/manifest.f4m?n=20&b=496,896,1296,1896"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["hdnea", "invalid"],
                "keys_status": False,
                "result": "http://example.com/i/master.m3u8?__b__=240&b=240,120,64,496,896,1296,1896&n=10"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["invalid"],
                "keys_status": False,
                "result": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896"
            },
            {
                "url": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123&n=20&b=496,896,1296,1896",
                "keys": ["n", "b"],
                "keys_status": False,
                "result": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123"
            },
            {
                "url": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123&n=20&b=496,896,1296,1896",
                "keys": ["hdnea"],
                "keys_status": True,
                "result": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["hdnea", "invalid"],
                "keys_status": True,
                "result": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["invalid"],
                "keys_status": True,
                "result": "http://example.com/i/master.m3u8"
            },
            {
                "url": "http://example.com/z/manifest.f4m?hdnea=st=123~exp=123~acl=/*~hmac=123&n=20&b=496,896,1296,1896",
                "keys": ["hdnea"],
                "keys_status": False,
                "new_dict": {"FOO": "BAR"},
                "result": "http://example.com/z/manifest.f4m?n=20&b=496,896,1296,1896&FOO=BAR"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["invalid"],
                "keys_status": True,
                "new_dict": {"FOO": "BAR"},
                "result": "http://example.com/i/master.m3u8?FOO=BAR"
            },
            {
                "url": "http://example.com/i/master.m3u8?hdnea=st=123~exp=123~acl=/*~hmac=123&n=10&__b__=240&b=240,120,64,496,896,1296,1896",
                "keys": ["invalid"],
                "keys_status": True,
                "new_dict": {"FOO": "BAR", "FOO2": "BAR2"},
                "result": "http://example.com/i/master.m3u8?FOO=BAR&FOO2=BAR2"
            },
        ]
        for test_dict in test_data:
            self.assertDictEqual(
                dict(parse_qsl(urlparse(test_dict["result"]).query)),
                dict(parse_qsl(urlparse(filter_urlquery(test_dict["url"], test_dict["keys"],
                                                        test_dict["keys_status"], test_dict.get("new_dict", {}))).query)))

    def test_prepend_www(self):
        self.assertEqual("http://www.test.se/test",
                         prepend_www("http://test.se/test"))
        self.assertEqual("http://www.test.se",
                         prepend_www("http://www.test.se"))

    def test_parse_json(self):
        self.assertEqual({}, parse_json("{}"))
        self.assertEqual({"test": 1}, parse_json("""{"test": 1}"""))
        self.assertEqual({"test": 1}, parse_json("""{"test": 1}""", schema=validate.Schema({"test": 1})))
        self.assertRaises(PluginError, parse_json, """{"test: 1}""")
        self.assertRaises(IOError, parse_json, """{"test: 1}""", exception=IOError)
        self.assertRaises(PluginError, parse_json, """{"test: 1}""" * 10)

    def test_parse_xml(self):
        expected = ET.Element("test", {"foo": "bar"})
        actual = parse_xml(u"""<test foo="bar"/>""", ignore_ns=True)
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.attrib, actual.attrib)

    def test_parse_xml_ns_ignore(self):
        expected = ET.Element("test", {"foo": "bar"})
        actual = parse_xml(u"""<test foo="bar" xmlns="foo:bar"/>""", ignore_ns=True)
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.attrib, actual.attrib)

    def test_parse_xml_ns(self):
        expected = ET.Element("{foo:bar}test", {"foo": "bar"})
        actual = parse_xml(u"""<h:test foo="bar" xmlns:h="foo:bar"/>""")
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.attrib, actual.attrib)

    def test_parse_xml_fail(self):
        self.assertRaises(PluginError,
                          parse_xml, u"1" * 1000)
        self.assertRaises(IOError,
                          parse_xml, u"1" * 1000, exception=IOError)

    def test_parse_xml_validate(self):
        expected = ET.Element("test", {"foo": "bar"})
        actual = parse_xml(u"""<test foo="bar"/>""",
                           schema=validate.Schema(xml_element(tag="test", attrib={"foo": text})))
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.attrib, actual.attrib)

    def test_parse_xml_entities_fail(self):
        self.assertRaises(PluginError,
                          parse_xml, u"""<test foo="bar &"/>""")

    def test_parse_xml_entities(self):
        expected = ET.Element("test", {"foo": "bar &"})
        actual = parse_xml(u"""<test foo="bar &"/>""",
                           schema=validate.Schema(xml_element(tag="test", attrib={"foo": text})),
                           invalid_char_entities=True)
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.attrib, actual.attrib)

    def test_parse_qsd(self):
        self.assertEqual(
            {"test": "1", "foo": "bar"},
            parse_qsd("test=1&foo=bar", schema=validate.Schema({"test": validate.text, "foo": "bar"})))

    def test_update_scheme(self):
        self.assertEqual(
            "https://example.com/foo",  # becomes https
            update_scheme("https://other.com/bar", "//example.com/foo")
        )
        self.assertEqual(
            "http://example.com/foo",  # becomes http
            update_scheme("http://other.com/bar", "//example.com/foo")
        )
        self.assertEqual(
            "http://example.com/foo",  # remains unchanged
            update_scheme("https://other.com/bar", "http://example.com/foo")
        )
        self.assertEqual(
            "https://example.com/foo",  # becomes https
            update_scheme("https://other.com/bar", "example.com/foo")
        )

    def test_time_to_offset(self):
        self.assertEqual(4953, time_to_offset("01h22m33s"))
        self.assertEqual(0, time_to_offset("123123fail"))

    def test_hours_minutes_seconds(self):
        self.assertEqual(4815, hours_minutes_seconds("01:20:15"))
