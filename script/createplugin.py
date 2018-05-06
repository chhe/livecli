#!/usr/bin/env python
''' Plugin Helper
    This script creates two new files with a basic plugin template and tests.
      - src/streamlink/plugins/classname.py
      - tests/test_plugin_classname.py

    usage: ./script/createplugin.py YourNewClassName
'''
from __future__ import print_function

import argparse
import os
import re
import sys

from textwrap import dedent

pkg_name = 'livecli'

data_plugin = '''import re\n
from {pkg}.plugin import Plugin
from {pkg}.plugin.api import http
from {pkg}.plugin.api import useragents
from {pkg}.stream import HLSStream\n
__livecli_docs__ = {{
    "domains": [
        "",
    ],
    "geo_blocked": [],
    "notes": "",
    "live": True,
    "vod": False,
    "last_update": "2018",
}}\n\n
class {classname}(Plugin):\n
    _url_re = re.compile(r'https?://(?:www\\.)?example\\.com/[^/]+')
    _hls_re = re.compile(r\'\'\'["'](?P<url>[^"']+\\.m3u8)["']\'\'\')\n
    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None\n
    def _get_streams(self):
        http.headers.update({{'User-Agent': useragents.FIREFOX}})
        res = http.get(self.url)\n
        m = self._hls_re.search(res.text)
        if not m:
            self.logger.debug('No video url found.')
            return\n
        hls_url = m.group('url')
        self.logger.debug('URL={{0}}'.format(hls_url))
        streams = HLSStream.parse_variant_playlist(self.session, hls_url)
        if not streams:
            return {{'live': HLSStream(self.session, hls_url)}}
        else:
            return streams\n\n
__plugin__ = {classname}\n'''

data_tests = '''import unittest\n
from {pkg}.plugins.{filename} import {classname}\n\n
class TestPlugin{classname}(unittest.TestCase):
    def test_can_handle_url(self):
        should_match = [
            '',
            '',
        ]
        for url in should_match:
            self.assertTrue({classname}.can_handle_url(url))\n
        should_not_match = [
            'https://example.com/index.html',
        ]
        for url in should_not_match:
            self.assertFalse({classname}.can_handle_url(url))\n'''


def setup_args():
    parser = argparse.ArgumentParser(
        prog='Create a new Plugin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='./script/createplugin.py YourNewClassName',
        description=dedent('''
        It will create two new files
            src/streamlink/plugins/classname.py
            tests/test_plugin_classname.py
        ''')
    )
    parser.add_argument(
        'name',
        metavar='ClassName',
        help='Python ClassName e.g. YouTube'
    )
    args, unknown = parser.parse_known_args()
    return args


def prompt(query):
    sys.stdout.write('create {0} ? [y/N]: '.format(query))
    try:
        answer = input()
    except Exception:
        answer = ""

    if answer.lower() in ('1', 't', 'true', 'y', 'yes'):
        return True
    else:
        return False


def ask_prompt(filepath):
    try:
        if os.path.exists(filepath):
            print('Skip - File {0} already exists.'.format(filepath))
            return False
        else:
            return prompt(filepath)
    except KeyboardInterrupt:
        sys.exit(130)


def create_new_file(filepath, data):
    f = open(filepath, 'w')
    f.write(data)
    f.close()


def main():
    if not os.getcwd().endswith(pkg_name):
        print('This script can only be used in the main {0} folder'.format(pkg_name))
        sys.exit(1)

    args = setup_args()
    if not args:
        sys.exit(1)

    class_name = args.name
    valid_name_re = re.compile(r'''^[a-zA-Z_][a-zA-Z0-9_]*$''')
    m = valid_name_re.match(class_name)
    if not m:
        print('invalid ClassName, make sure it matches the regex.')
        return

    plugin_name = args.name.lower()

    file_plugin = os.path.join(os.getcwd(), 'src', pkg_name, 'plugins', '{0}.py'.format(plugin_name))
    file_tests = os.path.join(os.getcwd(), 'tests', 'test_plugin_{0}.py'.format(plugin_name))

    for _file, _data in [(file_plugin, data_plugin), (file_tests, data_tests)]:
        status = ask_prompt(_file)
        if status:
            create_new_file(_file, _data.format(
                pkg=pkg_name,
                filename=plugin_name,
                classname=class_name,
            ))


if __name__ == '__main__':
    main()
