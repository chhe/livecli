# [Livecli][livecli-website]

[![TravisCI build status][travisci-build-status-badge]][travisci-build-status] [![codecov.io][codecov-coverage-badge]][codecov-coverage] [![pypi.python.org][pypi-badge]][pypi]

- Website: https://livecli.github.io/index.html
- Latest release: https://github.com/livecli/livecli/releases/latest
- GitHub: https://github.com/livecli/livecli
- Issue tracker: https://github.com/livecli/livecli/issues
- PyPI: https://pypi.python.org/pypi/livecli
- Free software: Simplified BSD license

Livecli is a _Command-line interface_ utility that pipes videos from online streaming services to a variety of video players.

The main purpose of livecli is to convert CPU-heavy flash plugins to a less CPU-intensive format,
also allow to watch livestreams on less powerful devices.

Livecli is a fork of the [Streamlink][streamlink] and [Livestreamer][livestreamer] project,

#### The advantages of Livecli:

- build in plugin that will try to open a stream on every website.
- fully compatible with [Kodi Leia](https://github.com/livecli/livecli#kodi)
- pycryptodomex can be used
- some new plugins
- [more commands](https://livecli.github.io/cli.html#command-line-usage)

# [Installation][livecli-installation]

#### Installation via Python pip

```bash
pip install --user livecli
```

This will install livecli as a normal user, not as root.
You might have to add `$HOME/.local/bin` to your `$PATH`

open `~/.bashrc` or `~/.bash_profile` or `~/.profile` and add

```sh
PATH="$HOME/.local/bin:$PATH"
```

#### Manual installation via Python

```bash
git clone https://github.com/livecli/livecli
cd livecli
pip install --user -U .
```

This will install livecli as a normal user, not as root.
You might have to add `$HOME/.local/bin` to your `$PATH`

open `~/.bashrc` or `~/.bash_profile` or `~/.profile` and add

```sh
PATH="$HOME/.local/bin:$PATH"
```

# Features

Livecli is built via a plugin system which allows new services to be easily added.

Supported streaming services, among many others, are:

- [Dailymotion](https://www.dailymotion.com)
- [Livestream](https://livestream.com)
- [Twitch](https://www.twitch.tv)
- [UStream](http://www.ustream.tv)
- [YouTube Live](https://www.youtube.com)

A list of all supported plugins can be found on the [plugin page][livecli-plugins].


# Quickstart

After installing, simply use:

```
livecli STREAMURL best
```

Livecli will automatically open the stream in its default video player!
See [Livecli's detailed documentation][livecli-documentation] for all available configuration options,
CLI parameters and usage examples.

# Kodi

Livecli can be used with Kodi Leia, it can be installed from the [Livecli Kodi Repository][kodi-repo].

For more information see [service.livecli.proxy][service.livecli.proxy]

# Contributing

All contributions are welcome.
Feel free to open a new thread on the issue tracker or submit a new pull request.
Please read [CONTRIBUTING.md][contributing] first. Thanks!


  [livecli-website]: https://livecli.github.io
  [livecli-plugins]: https://livecli.github.io/plugin_matrix.html
  [livecli-documentation]: https://livecli.github.io/cli.html
  [livecli-installation]: https://livecli.github.io/install.html
  [livecli-installation-windows]: https://livecli.github.io/install.html#windows-binaries
  [livecli-installation-windows-portable]: https://livecli.github.io/install.html#windows-portable-version
  [livecli-installation-linux]: https://livecli.github.io/install.html#linux-and-bsd-packages
  [livecli-installation-others]: https://livecli.github.io/install.html#other-platforms
  [streamlink]: https://github.com/streamlink/streamlink
  [livestreamer]: https://github.com/chrippa/livestreamer
  [contributing]: https://github.com/livecli/livecli/blob/master/CONTRIBUTING.md
  [changelog]: https://github.com/livecli/livecli/blob/master/CHANGELOG.rst
  [contributors]: https://github.com/livecli/livecli/graphs/contributors
  [travisci-build-status]: https://travis-ci.org/livecli/livecli
  [travisci-build-status-badge]: https://api.travis-ci.org/livecli/livecli.svg?branch=master
  [pypi]: https://pypi.python.org/pypi/livecli
  [pypi-badge]: https://img.shields.io/pypi/v/livecli.svg?style=flat-square
  [service.livecli.proxy]: https://github.com/livecli/service.livecli.proxy
  [kodi-repo]: https://github.com/livecli/repo
  [codecov-coverage]: https://codecov.io/gh/livecli/livecli
  [codecov-coverage-badge]: https://codecov.io/gh/livecli/livecli/branch/master/graph/badge.svg
