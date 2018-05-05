livecli 3.9.0 (2018-05-05)
--------------------------
Livecli 3.9.0 has been released!

See below for further information.

New

::

    [docs] Added ./script/createplugin.py guide
    [docs] Added a Guide of how Livecli can be used with a Browser
    [FC2] new plugin for https://live.fc2.com
    [hls] allow invalid PROGRAM-ID
    [RUtube] new plugin for https://rutube.ru
    [TLCtr] new plugin for https://www.tlctv.com.tr/canli-izle

Updates

::

    [ABweb] changes for site update
    [app17] Fix HLS URL
    [filmon] Fix for 404 error - invalid channel name
    [flake8] W504 line break after binary operator
    [flake8] W605 invalid escape sequence
    [ITV] Small tweaks to fix ITV player.
    [RaiPlay] set User-Agent header, print geo block message
    [script] update headers for plugin create script
    [Twitch] updated api client id for --twitch-oauth-authenticate

livecli 3.8.0 (2018-04-21)
--------------------------
Livecli 3.8.0 has been released!

See below for further information.

::

    [ABweb] New plugin for BIS Livestreams of french AB Groupe
    [build] Fixed appveyor build pip10 error (#21)
    [docs] documentation update
    [gardenersworld] removed, it was broken and works now with resolve.py
    [hls] stream.hls: change --hls-audio-select to take a list and wildcard
    [resolve] add url to debug message
    [script] added sha256sum check for makeinstaller
    [script] automate release changelog text
    [server] update option hls-audio-select
    [server] update plugin commands
    [tv4play] removed outdated plugin
    [tv8cat] removed - it can be used with the resolve.py plugin
    [TVP] New Plugin for Telewizja Polska S.A.
    [utils] add examples for filter_urlquery
    [utils] new method seconds_to_hhmmss, used for hls segment time debug
    [vk] Fixed regex for video sources
    [zattoo] set self._expires cache correctly

livecli 3.7.0 (2018-04-02)
--------------------------
Livecli 3.7.0 has been released!

For more details see below.

::

    [api] useragents update
    [bintray] Removed unused bintray scripts
    [docs] Added E2 ipk to Livecli Applications and Kodi update
    [docs] Added for Sideloading plugins the Linux and Kodi paths.
    [docs] New icon and enabled favicon.ico
    [hls] Added more debug messages for hls-session-reload
    [livecli_cli] removed duplicate code for NamedPipe
    [option] Added retry-max option to limit the number of fetch retries.
    [Plugin] changed default_stream_types to "hls,hds,rtmp,http,*"
    [plugins] Removed common_jwplayer, not used old code.
    [plugins] Removed common_swf, not used old code.
    [resolve] Fixed IndexError: list index out of range
    [rtve] add an option to parse_xml to try to fix invalid character entities
    [server] allow `stream-types`
    [server] allow 301 redirect for HLS and HTTP streams
    [server] allow different qualitys
    [server] allow MuxedStreams
    [server] changed wrong plugin option --resolve-turn-off
    [server] use str in list instead of not working == (str or str)
    [tests] Added some tests and Flake8
    [tests] DeprecationWarning: Please use assertRegex instead.
    [tests] Don't use possibly closed file with load_module
    [TF1] Added HD streams for https://www.tf1.fr/tf1/direct
    [tga] removed rtmp streams, updated domains
    [ustreamtv] stop api calls if a stream ends
    [utils] New option to filter urlquerys
    [vaughnlive] changed rtmp server IP
    [vk] Fix for new urls

livecli 3.6.0 (2018-03-19)
--------------------------
Livecli 3.6.0 has been released!

For more details see below.

::

    [pixiv] Added login option
    [plugin] Removed Plugin.get_streams use Plugin.streams
    [readme] replace .md with .rst
    [resolve] better iframe handling
    [resolve] moved code
    [resolve] use http.headers instead of self.headers
    [server] allow 0.0.0.0 as HOST and new cmd --server-host
    [server] Fixed HDS support
    [tests] resolve - AttributeError: 'NoneType' object has no attribute
    [youtube] Don't use MuxedStream for livestreams
    Removed some Deprecated livestreamer options

livecli 3.5.0 (2018-03-14)
--------------------------
Livecli 3.5.0 has been released!

For more details see below.

::

    [api] Useragents update.
    [balticlivecam] better debug msg update
    [changelog] removed names and emails, removed old changelogs
    [codecov] use pytest and upload real data
    [compat] Remove unused imports
    [compat] Removed unused shlex_quote
    [dailymotion] Fix for new stream data API
    [docs] fix table layout on the install page
    [docs] updated AUTHORS, removed duplicates and removed not used script
    [dogan] cleanup url_re and better debug
    [huya] cleanup
    [IDF1] Add support for IDF1
    [pixiv] New plugin for sketch.pixiv.net
    [resolve] new cmd --resolve-turn-off
    [resolve] moved _iframe_re _playlist_re _rtmp_re into a common file
    [resolve] moved lists and dicts into the class / self
    [resolve] remove Cache use a python class as Cache
    [resolve] Remove invalid scheme urls
    [resolve] static blacklist update
    [resolve] whitelist_endswith for playlists and don't allow {} for urls
    [script] New script that creates a basic plugin template with tests.
    [sportschau] Fixed plugin.
    [streann] Fixed broken plugin
    [tests] Added new Plugin tests.

livecli 3.4.0 (2018-02-21)
--------------------------
Livecli 3.4.0 has been released!

- some Plugins fixed
- cleanup / changes to docs

For more details see below.

::

    [aftonbladet] Fix for tv.aftonbladet.se
    [artetv] update for some languages
    [docs] removed unnecessary text from CONTRIBUTING.md, revert pip --user
    [dplay] Fixed Plugin.
    [earthcam] Fix for HLS streams
    [kanal7] Fix for kanal7.com/canli-izle, website changed again
    [ovvatv] Fix for new domain, resolve.py will now search for the iframe
    [plugins] Removed Plugins, most of them will now use resolve.py
    [resolve] Add twitter widgets to blacklist and livecli_docs update
    [resolve] better debug message for an invalid playlist url
    [resolve] re.DOTALL for iframe regex and new domain for blacklist
    [resolve] use the last self.url as a Referer for the playlist urls.
    [ruv] Fixed Plugin, use api for livestreams and use resolve.py for vods
    [server] allow only http based streams: HDS HLS HTTP
    [server] Fixed TypeError: unhashable type: 'list' for custom Plugins
    [vaughnlive] Fix for rtmp_server
    [vgtv] moved aftonbladet.se into vgtv.py and fixed vgtv.no
    [younow] cleanup python code
    New Plugin for balticlivecam.com
    Removed dead or not wanted plugins

livecli 3.3.0 (2018-02-14)
--------------------------
Livecli 3.3.0 has been released!

- New command --server to start a local Livecli server
- New option --resolve-whitelist-netloc for iframes
- New option --resolve-whitelist-path for iframes
- Plugins updates

For more details see below.

::

    [bigo] remove session-reload, playlists are working again
    [docs] small updates on .md files
    [docs] use always the last release version not the git tag, meta data
    [dogan] Fix for teve2.com.tr/canli-yayin
    [install] recommend pip install --user instead of sudo and README update
    [kanal7] Fix for kanal7.com/canli-izle
    [logger] allow a prefix message for the log output
    [looch] url_re update
    [mediaklikk] Fixed plugin livestream, vod and radio
    [plugins] marked some plugins as broken and removed expressen plugin ...
    [resolve] Fixed compare_url_path
    [resolve] made the playlist removal better and fixed expressen.se
    [resolve] update ad regex and small plugin docs update.
    [resolve] whitelist commands, _make_url_list cleanup with better debug log
    [server] New command to start a local Livecli server
    [tests] Fixed metaclass for test_plugins.py on python 3
    [tests] resolve - _make_url_list
    [tests] resolve and log tests, removed not used Kodi import
    [TF1] channel maps update.
    [travis] fixed Codevov for travis
    [tv3cat] fixed url validate schema
    [zattoo] Added support for zattoo recordings
    Removed DeprecationWarning: inspect.getargspec() is deprecated
    Removed Plugins, all of them should be covered by resolve.py

livecli 3.2.0 (2018-02-07)
--------------------------
Livecli 3.2.0 has been released!

- New option --hls-key-uri
- resolve plugin updates
- Kodi version will be released now on https://github.com/livecli/repo

For more details see below.

::

    [compat] Renamed imports to compat_X
    [compat] use a crypto prefix for Crypto and Cryptodome
    [compat] use Cryptodome before Crypto
    [docs] made the path detection for build_path better
    [docs] Removed message.
    [flake8] __all__
    [hls] Fixed bug TypeError: 'bool' object is not callable
    [hls] New option --hls-key-uri
    [hls] ression reload better update
    [inter] New Plugin for - inter.ua - k1.ua - ntn.ua
    [Kodi] support different Importpaths for Kodi and Flake8 for webtv
    [output] New options to download a stream --auto-output
    [resolve] _unescape_iframe_re improved
    [resolve] playlist url's with ;\s after the filetype are now invalid
    [resolve] Remove 127.0.0.1 from valid playlist urls.
    [resolve] use only 2 sec for cache url
    [resolve] use urlparse to filter the correct playlist url
    [travis] use pip install -U .
    [viasat] don't close if swf_url is invalid, regex update
    [zattoo] use requests instead of http, so no session will be used.

livecli 3.1.1 (2018-01-23)
--------------------------
Livecli 3.1.1 has been released!

- Added a resolve plugin that will try to find a valid url on every website,
  it has a built in blacklist feature.
- pycryptodomex can now be used
- Removes bug of an invisible terminal after ffmpeg got killed.
- Added some new Plugins

For more details see below.

::

    [bigo] hls-session-reload and hls-segment-ignore-number will be used
    [docs] get the latest version from github tags
    [docs] plugin_matrix automation part 1/2
    [docs] plugin_matrix automation part 2/2
    [docs] Removed dead plugin moved hitbox.py to smashcast.py
    [docs] Removed python 2.6 and readme update.
    [ffmpeg] Removes bug of an invisible terminal after ffmpeg got killed.
    [hls] New option --hls-segment-ignore-number
    [hls] New option --hls-session-reload
    [myfreecams] New Plugin for myfreecams.com
    [okru] New Plugin for ok.ru
    [PerviyKanal] New Plugin for 1tv.ru/live
    [resolve] Added Plugin that will try to resolve every website.
    [resolve] don't add self.url to _make_url_list
    [resolve] moved the netloc/path blacklist into _make_url_list
    [resolve] New Plugin option --resolve-blacklist-netloc
    [resolve] New Plugin option --resolve-blacklist-path
    [resolve] removes .jpg .png and .svg at the end of a path as a valid url
    [rtbf] New Plugin for rtbf.be
    [scripts] exit the release script properly if something is missing
    [smashcast] fixed http urls
    [tests] Fixed tests temporarily.
    [welt] New Plugin for welt.de
    Allow flake8 to fail, README pip update and removed old livestreamer versionchanges.
    Allow the use of pycryptodomex and removed is_py33 from compat
    is_win32: use 'from livecli.compat import is_win32'
    Moved hours_minutes_seconds into livecli.utils
    Removed deprecated functions

livecli 3.0.0 (2018-01-18)
--------------------------
Livecli 3.0.0 has been released!

I forked streamlink and changed the name to livecli.

- livestreamer = 1.0
- streamlink = 2.0
- livecli = 3.0

I updated some plugins and removed dead plugins,
for more details see below.

::

    [afreeca] Plugin update.
    [bbciplayer] Fix authentication failures
    [BTV] Fixed login return message
    [build] Added external assets
    [build] Fixed script/release.sh for versioneer
    [camsoda] Fixed broken plugin
    [canalplus] Update plugin according to website changes
    [cli-debug] Show current installed versions with -l debug
    [Dailymotion] Fixed livestream id from channelpage
    [docs] changed deploy-key
    [docs] Fix various typos in comments and documentation
    [docs] remove flattr-badge.png image
    [docs] Removed dead plugins.
    [docs] Removed doggo.ico
    [docs] Removed MPlayer2 - Domain expired - Not maintained anymore
    [docs] Removed opencollective
    [docs] use normal version for docs
    [docs] Welcome 2018
    [Douyutv] fix API
    [hls] Don't try to skip a stream if the offset is 0
    [hls] Implement PKCS#7 padding decoding with AES-128 HLS
    [hls] New option --hls-segment-ignore-names
    [mitele] Update for different api response - fallback if not hls_url was found, just the suffix
    [mixer] moved beam.py to mixer.py file requires two commits, for a proper commit history
    [mixer] replaced beam.pro with mixer.com
    [mlgtv] Fixed broken Plugin streamlink/streamlink#1362
    [periscope] Update for hls variant playlists
    [picarto] Reworked picarto.tv plugin to deal with website changes.
    [pluzz] Fix video ID regex for France 3 Régions streams
    [qq] New Plugin for live.qq.com
    [streann] Added headers for post request
    [tests] Fixed decrypt test and removed DeprecationWarning
    [tigerdile] Added tigerdile HLS support and proper API poll for offline streams.
    [travis] disabled bintray
    [travis] run flake8
    [tvrplus] hls regex update and send a Referer
    [twitch and youtube] open hls-start-offset for urls with a time automatically
    [viasat] Added support for urls without a stream_id
    [youtube] added Audio m4a itag 256 and 258
    [youtube] New params for get_video_info
    [zdf] apiToken update
    [zengatv] New Plugin for zengatv.com
    Add plugin for olympicchannel.com
    build: remove broken "latest" config for bintray
    build: use versioneer to set the build number
    docs: rewrite Windows binaries install section
    EOL Python 3.3
    fix plugin for bilibili to adapt the new API
    hls: add absolute start offset and duration options to the HLStream API
    nsis: restore old install dir, keep multiuser
    plugins.huya: fix stream URL scheme prefix
    plugins.kanal7: update to stream player URL config
    plugins.vaughnlive: updated rtmp server map
    stream.hls: add option to restart live stream, if possible
    stream.hls: add options to skip some time at the start/end of VOD streams
    stream.hls: remove the end offset and replace with duration
