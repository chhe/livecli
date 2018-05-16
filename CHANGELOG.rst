livecli 3.9.0 (2018-05-05)
--------------------------
Livecli 3.9.0 has been released!

**Added Plugin**

  - [FC2] new plugin for https://live.fc2.com
  - [RUtube] new plugin for https://rutube.ru
  - [TLCtr] new plugin for https://www.tlctv.com.tr/canli-izle

**Changed**

  - [hls] allow invalid PROGRAM-ID

**Fixed Plugin**

  - [ABweb] changes for site update
  - [app17] Fix HLS URL
  - [filmon] Fix for 404 error - invalid channel name
  - [ITV] Small tweaks to fix ITV player.
  - [RaiPlay] set User-Agent header, print geo block message
  - [Twitch] updated api client id for --twitch-oauth-authenticate

livecli 3.8.0 (2018-04-21)
--------------------------
Livecli 3.8.0 has been released!

**Added**

  - [utils] new method seconds_to_hhmmss, used for hls segment time debug
  - [utils] add examples for filter_urlquery

**Added Plugin**

  - [ABweb] New plugin for BIS Livestreams of french AB Groupe

**Changed**

  - [hls] stream.hls: change --hls-audio-select to take a list and wildcard
  - [server] update plugin commands

**Fixed Plugin**

  - [zattoo] set self._expires cache correctly
  - [vk] Fixed regex for video sources
  - [TVP] New Plugin for Telewizja Polska S.A.

**Removed**

  - [gardenersworld] removed, it was broken and works now with resolve.py
  - [tv8cat] removed - it can be used with the resolve.py plugin
  - [tv4play] removed outdated plugin

livecli 3.7.0 (2018-04-02)
--------------------------
Livecli 3.7.0 has been released!

**Added**

  - [docs] Added E2 ipk to Livecli Applications and Kodi update
  - [docs] Added for Sideloading plugins the Linux and Kodi paths.
  - [option] Added retry-max option to limit the number of fetch retries.
  - [server] allow `stream-types`
  - [server] allow 301 redirect for HLS and HTTP streams
  - [server] allow different qualitys
  - [server] allow MuxedStreams
  - [utils] New option to filter urlquerys

**Added Plugin**

  - [TF1] Added HD streams for https://www.tf1.fr/tf1/direct

**Changed**

  - [api] useragents update
  - [hls] Added more debug messages for hls-session-reload
  - [Plugin] changed default_stream_types to "hls,hds,rtmp,http,\*"

**Fixed**

  - [server] use str in list instead of not working == (str or str)

**Fixed Plugin**

  - [resolve] Fixed IndexError: list index out of range
  - [rtve] add an option to parse_xml to try to fix invalid character entities
  - [tga] removed rtmp streams, updated domains
  - [ustreamtv] stop api calls if a stream ends
  - [vaughnlive] changed rtmp server IP
  - [vk] Fix for new urls

**Removed**

  - [livecli_cli] removed duplicate code for NamedPipe
  - Removed common_jwplayer
  - Removed common_swf

livecli 3.6.0 (2018-03-19)
--------------------------
Livecli 3.6.0 has been released!

**Added**

  - [server] allow 0.0.0.0 as HOST and new cmd --server-host

**Added Plugin**

  - [pixiv] Added login option

**Fixed**

  - [server] Fixed HDS support

**Fixed Plugin**

  - [resolve] better iframe handling
  - [youtube] Don't use MuxedStream for livestreams

**Removed**

  - [plugin] Removed Plugin.get_streams use Plugin.streams
  - Removed some Deprecated livestreamer options

livecli 3.5.0 (2018-03-14)
--------------------------
Livecli 3.5.0 has been released!

**Added**

  - [script] New script that creates a basic plugin template with tests.

**Added Plugin**

  - [IDF1] Add support for IDF1
  - [pixiv] New plugin for sketch.pixiv.net
  - [resolve] new cmd --resolve-turn-off

**Changed**

  - [api] Useragents update.

**Fixed Plugin**

  - [balticlivecam] better debug msg update
  - [dailymotion] Fix for new stream data API
  - [dogan] cleanup url_re and better debug
  - [huya] cleanup
  - [resolve] remove Cache use a python class as Cache
  - [resolve] Remove invalid scheme urls
  - [resolve] static blacklist update
  - [resolve] whitelist_endswith for playlists and don't allow {} for urls
  - [sportschau] Fixed plugin.
  - [streann] Fixed broken plugin

**Removed**

  - [compat] Remove unused imports

livecli 3.4.0 (2018-02-21)
--------------------------
Livecli 3.4.0 has been released!

**Added Plugin**

  - [balticlivecam] New Plugin for balticlivecam.com

**Fixed**

  - [server] Fixed TypeError: unhashable type: 'list' for custom Plugins
  - [server] allow only http based streams: HDS HLS HTTP

**Fixed Plugin**

  - [aftonbladet] Fix for tv.aftonbladet.se
  - [artetv] update for some languages
  - [dplay] Fixed Plugin
  - [earthcam] Fix for HLS streams
  - [kanal7] Fix for kanal7.com/canli-izle
  - [ovvatv] Fix for new domain
  - [resolve] Add twitter widgets to blacklist and livecli_docs update
  - [resolve] better debug message for an invalid playlist url
  - [resolve] re.DOTALL for iframe regex and new domain for blacklist
  - [resolve] use the last self.url as a Referer for the playlist urls.
  - [ruv] Fixed Plugin
  - [vaughnlive] Fix for rtmp_server
  - [vgtv] moved aftonbladet.se into vgtv.py and fixed vgtv.no
  - [younow] cleanup python code

**Removed**

  - Removed dead, not wanted plugins and some might work with resolve.py

livecli 3.3.0 (2018-02-14)
--------------------------
Livecli 3.3.0 has been released!

**Added**

  - [logger] allow a prefix message for the log output
  - [server] New command to start a local Livecli server

**Added Plugin**

  - [resolve] new command --resolve-whitelist-netloc
  - [resolve] new command --resolve-whitelist-path
  - [zattoo] Added support for zattoo recordings

**Changed**

  - Removed DeprecationWarning: inspect.getargspec() is deprecated

**Fixed Plugin**

  - [bigo] remove session-reload, playlists are working again
  - [dogan] Fix for teve2.com.tr/canli-yayin
  - [kanal7] Fix for kanal7.com/canli-izle
  - [looch] url_re update
  - [mediaklikk] Fixed plugin livestream, vod and radio
  - [resolve] made the playlist removal better
  - [resolve] update ad regex
  - [TF1] channel maps update.
  - [tv3cat] fixed url validate schema

**Deprecated**

  - marked some plugins as broken

**Removed**

  - Removed Plugins, all of them should be covered by resolve.py

livecli 3.2.0 (2018-02-07)
--------------------------
Livecli 3.2.0 has been released!

**Added**

  - [output] New options to download a stream --auto-output
  - [Kodi] support different Importpaths for Kodi
  - [hls] New option --hls-key-uri

**Added Plugin**

  - [inter] New Plugin for - inter.ua - k1.ua - ntn.ua

**Changed**

  - [compat] Renamed imports to compat_X
  - [compat] use a crypto prefix for Crypto and Cryptodome
  - [compat] use Cryptodome before Crypto

**Fixed**

  - [hls] changed the session reload url update
  - [hls] Fixed bug TypeError: 'bool' object is not callable

**Fixed Plugin**

  - [resolve] _unescape_iframe_re improved
  - [resolve] playlist url's with ;\s after the filetype are now invalid
  - [resolve] use urlparse to filter the correct playlist url
  - [viasat] don't close if swf_url is invalid, regex update
  - [zattoo] use requests instead of http, so no session will be used.

livecli 3.1.1 (2018-01-23)
--------------------------
Livecli 3.1.1 has been released!

**Added**

  - [hls] New option --hls-segment-ignore-number
  - [hls] New option --hls-session-reload
  - [resolve] New Plugin option --resolve-blacklist-netloc
  - [resolve] New Plugin option --resolve-blacklist-path

**Added Plugin**

  - [myfreecams] New Plugin for myfreecams.com
  - [okru] New Plugin for ok.ru
  - [PerviyKanal] New Plugin for 1tv.ru/live
  - [resolve] Added Plugin that will try to resolve every website.
  - [rtbf] New Plugin for rtbf.be
  - [welt] New Plugin for welt.de

**Changed**

  - [docs] plugin_matrix automation
  - Allow the use of pycryptodomex
  - Moved hours_minutes_seconds into livecli.utils

**Fixed**

  - [ffmpeg] Removes bug of an invisible terminal after ffmpeg got killed.
  - [scripts] exit the release script properly if something is missing

**Fixed Plugin**

  - [bigo] hls-session-reload and hls-segment-ignore-number will be used
  - [smashcast] fixed http urls

**Removed**

  - [docs] Removed dead plugin
  - [docs] Removed python 2.6
  - Removed deprecated functions
  - removed old livestreamer versionchanges

livecli 3.0.0 (2018-01-18)
--------------------------
Livecli 3.0.0 has been released!

I forked streamlink and changed the name to livecli.

- livestreamer = 1.0
- streamlink = 2.0
- livecli = 3.0

**Added**

  - [build] Added external assets
  - [build] use versioneer to set the build number
  - [cli-debug] Show current installed versions with -l debug
  - [hls] add absolute start offset and duration options to the HLStream API
  - [hls] add option to restart live stream, if possible
  - [hls] add options to skip some time at the start/end of VOD streams
  - [hls] New option --hls-segment-ignore-names

**Added Plugin**

  - [olympicchannel] Add plugin for olympicchannel.com
  - [qq] New Plugin for live.qq.com
  - [twitch and youtube] open hls-start-offset for urls with a time automatically
  - [zengatv] New Plugin for zengatv.com

**Changed**

  - [hls] Implement PKCS#7 padding decoding with AES-128 HLS

**Fixed**

  - [hls] Don't try to skip a stream if the offset is 0
  - [nsis] restore old install dir, keep multiuser

**Fixed Plugin**

  - [afreeca] Plugin update.
  - [bbciplayer] Fix authentication failures
  - [bilibili] fix plugin for bilibili to adapt the new API
  - [BTV] Fixed login return message
  - [camsoda] Fixed broken plugin
  - [canalplus] Update plugin according to website changes
  - [Dailymotion] Fixed livestream id from channelpage
  - [Douyutv] fix API
  - [huya] fix stream URL scheme prefix
  - [kanal7] update to stream player URL config
  - [mitele] Update for different api response
  - [mixer] replaced beam.pro with mixer.com
  - [mlgtv] Fixed broken Plugin
  - [periscope] Update for hls variant playlists
  - [picarto] Reworked picarto.tv plugin to deal with website changes.
  - [pluzz] Fix video ID regex for France 3 Régions streams
  - [streann] Added headers for post request
  - [tigerdile] Added HLS support and proper API poll for offline streams.
  - [tvrplus] hls regex update and send a Referer
  - [vaughnlive] updated rtmp server map
  - [viasat] Added support for urls without a stream_id
  - [youtube] added Audio m4a itag 256 and 258
  - [youtube] New params for get_video_info
  - [zdf] apiToken update

**Deprecated**

  - Python 2.6 / 3.3 is not supported anymore

**Removed**

  - [docs] Removed dead plugins
  - [docs] Removed doggo.ico
