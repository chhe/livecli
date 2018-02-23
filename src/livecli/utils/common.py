import re

# Regex for: Iframes
_iframe_re = re.compile(r"""
    <ifr(?:["']\s?\+\s?["'])?ame
    (?!\sname=["']g_iFrame).*?src=
    ["'](?P<url>[^"']+)["']
    .*?(?:/>|>(?:[^<>]+)?
    </ifr(?:["']\s?\+\s?["'])?ame(?:\s+)?>)
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)

# Regex for: .f4m and .m3u8 files
_playlist_re = re.compile(r"""
    (?:["']|=|&quot;)(?P<url>
        (?<!title=["'])
            [^"'<>\s\;]+\.(?:m3u8|f4m|mp3|mp4|mpd)
        (?:[^"'<>\s\\]+)?)
    (?:["']|(?<!;)\s|>|\\&quot;)
    """, re.DOTALL | re.VERBOSE)

# Regex for: rtmp
_rtmp_re = re.compile(r"""["'](?P<url>rtmp(?:e|s|t|te)?://[^"']+)["']""")

__all__ = [
    "_iframe_re",
    "_playlist_re",
    "_rtmp_re",
]
