import os
import re
import unittest

from six import assertRegex

from livecli.plugin.plugin import HIGH_PRIORITY, LOW_PRIORITY

from livecli import Livecli
from livecli import NoPluginError
from livecli.plugins import Plugin
from livecli.stream import AkamaiHDStream
from livecli.stream import HLSStream
from livecli.stream import HTTPStream
from livecli.stream import RTMPStream


class TestSession(unittest.TestCase):
    PluginPath = os.path.join(os.path.dirname(__file__), "plugins")

    def setUp(self):
        self.session = Livecli()
        self.session.load_plugins(self.PluginPath)

    def test_exceptions(self):
        try:
            # Turn off the resolve.py plugin
            self.session.set_plugin_option("resolve", "turn_off", True)
            self.session.resolve_url("invalid url")
            self.assertTrue(False)
        except NoPluginError:
            self.assertTrue(True)

    def test_load_plugins(self):
        plugins = self.session.get_plugins()
        self.assertTrue(plugins["testplugin"])

    def test_builtin_plugins(self):
        plugins = self.session.get_plugins()
        self.assertTrue("twitch" in plugins)

    def test_resolve_url(self):
        plugins = self.session.get_plugins()
        plugin = self.session.resolve_url("http://test.se/channel")
        self.assertTrue(isinstance(plugin, Plugin))
        self.assertTrue(isinstance(plugin, plugins["testplugin"]))

    def test_resolve_url_priority(self):
        from tests.plugins.testplugin import TestPlugin

        class HighPriority(TestPlugin):
            @classmethod
            def priority(cls, url):
                return HIGH_PRIORITY

        class LowPriority(TestPlugin):
            @classmethod
            def priority(cls, url):
                return LOW_PRIORITY

        self.session.plugins = {
            "test_plugin": TestPlugin,
            "test_plugin_low": LowPriority,
            "test_plugin_high": HighPriority,
        }
        plugin = self.session.resolve_url_no_redirect("http://test.se/channel")
        plugins = self.session.get_plugins()

        self.assertTrue(isinstance(plugin, plugins["test_plugin_high"]))
        self.assertEqual(HIGH_PRIORITY, plugin.priority(plugin.url))

    def test_resolve_url_no_redirect(self):
        plugins = self.session.get_plugins()
        plugin = self.session.resolve_url_no_redirect("http://test.se/channel")
        self.assertTrue(isinstance(plugin, Plugin))
        self.assertTrue(isinstance(plugin, plugins["testplugin"]))

    def test_options(self):
        self.session.set_option("test_option", "option")
        self.assertEqual(self.session.get_option("test_option"), "option")
        self.assertEqual(self.session.get_option("non_existing"), None)

        self.assertEqual(self.session.get_plugin_option("testplugin", "a_option"), "default")
        self.session.set_plugin_option("testplugin", "another_option", "test")
        self.assertEqual(self.session.get_plugin_option("testplugin", "another_option"), "test")
        self.assertEqual(self.session.get_plugin_option("non_existing", "non_existing"), None)
        self.assertEqual(self.session.get_plugin_option("testplugin", "non_existing"), None)

    def test_plugin(self):
        plugin = self.session.resolve_url("http://test.se/channel")
        streams = plugin.streams()

        self.assertTrue("best" in streams)
        self.assertTrue("worst" in streams)
        self.assertTrue(streams["best"] is streams["1080p"])
        self.assertTrue(streams["worst"] is streams["350k"])
        self.assertTrue(isinstance(streams["rtmp"], RTMPStream))
        self.assertTrue(isinstance(streams["http"], HTTPStream))
        self.assertTrue(isinstance(streams["hls"], HLSStream))
        self.assertTrue(isinstance(streams["akamaihd"], AkamaiHDStream))

    def test_plugin_stream_types(self):
        plugin = self.session.resolve_url("http://test.se/channel")
        streams = plugin.streams(stream_types=["http", "rtmp"])

        self.assertTrue(isinstance(streams["480p"], HTTPStream))
        self.assertTrue(isinstance(streams["480p_rtmp"], RTMPStream))

        streams = plugin.streams(stream_types=["rtmp", "http"])

        self.assertTrue(isinstance(streams["480p"], RTMPStream))
        self.assertTrue(isinstance(streams["480p_http"], HTTPStream))

    def test_plugin_stream_sorted_excludes(self):
        plugin = self.session.resolve_url("http://test.se/channel")
        streams = plugin.streams(sorting_excludes=["1080p", "3000k"])

        self.assertTrue("best" in streams)
        self.assertTrue("worst" in streams)
        self.assertTrue(streams["best"] is streams["1500k"])

        streams = plugin.streams(sorting_excludes=[">=1080p", ">1500k"])
        self.assertTrue(streams["best"] is streams["1500k"])

        streams = plugin.streams(sorting_excludes=lambda q: not q.endswith("p"))
        self.assertTrue(streams["best"] is streams["3000k"])

    def test_plugin_support(self):
        plugin = self.session.resolve_url("http://test.se/channel")
        streams = plugin.streams()

        self.assertTrue("support" in streams)
        self.assertTrue(isinstance(streams["support"], HTTPStream))

    def test_version(self):
        # PEP440 - https://www.python.org/dev/peps/pep-0440/
        VERSION_PATTERN = r"""
            v?
            (?:
                (?:(?P<epoch>[0-9]+)!)?                           # epoch
                (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
                (?P<pre>                                          # pre-release
                    [-_\.]?
                    (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
                    [-_\.]?
                    (?P<pre_n>[0-9]+)?
                )?
                (?P<post>                                         # post release
                    (?:-(?P<post_n1>[0-9]+))
                    |
                    (?:
                        [-_\.]?
                        (?P<post_l>post|rev|r)
                        [-_\.]?
                        (?P<post_n2>[0-9]+)?
                    )
                )?
                (?P<dev>                                          # dev release
                    [-_\.]?
                    (?P<dev_l>dev)
                    [-_\.]?
                    (?P<dev_n>[0-9]+)?
                )?
            )
            (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
        """

        _version_re = re.compile(
            r"^\s*" + VERSION_PATTERN + r"\s*$",
            re.VERBOSE | re.IGNORECASE,
        )

        assertRegex(self, self.session.version, _version_re)
