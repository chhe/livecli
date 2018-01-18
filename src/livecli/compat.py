import os
import sys

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)
is_win32 = os.name == "nt"

# win/nix compatible devnull
try:
    from subprocess import DEVNULL

    def devnull():
        return DEVNULL
except ImportError:
    def devnull():
        return open(os.path.devnull, 'w')

if is_py2:
    _str = str
    str = unicode  # noqa
    range = xrange  # noqa

    def bytes(b, enc="ascii"):
        return _str(b)

elif is_py3:
    bytes = bytes
    str = str
    range = range

try:
    from urllib.parse import (
        urlparse, urlunparse, urljoin, quote, unquote, parse_qsl, urlencode
    )
    import queue
except ImportError:
    from urlparse import urlparse, urlunparse, urljoin, parse_qsl
    from urllib import quote, unquote, urlencode
    import Queue as queue

try:
    from shutil import which
except ImportError:
    from backports.shutil_which import which

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher import Blowfish
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Util import number
except ImportError:
    from Cryptodome.Cipher import AES
    from Cryptodome.Cipher import Blowfish
    from Cryptodome.Cipher import PKCS1_v1_5
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Util import number


__all__ = [
    "AES",
    "Blowfish",
    "bytes",
    "devnull",
    "is_py2",
    "is_py3",
    "is_win32",
    "number",
    "parse_qsl",
    "PKCS1_v1_5",
    "queue",
    "quote",
    "range",
    "RSA",
    "str",
    "unquote",
    "urlencode",
    "urljoin",
    "urlparse",
    "urlunparse",
    "which",
]
