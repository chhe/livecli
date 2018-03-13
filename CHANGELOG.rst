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
