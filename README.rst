Livecli
=======

|TravisCI|

Livecli is a *Command-line* utility that pipes videos from
online streaming services to a variety of video players.

The main purpose of Livecli is to convert CPU-heavy websites to a
less CPU-intensive format.

Websites

-  GitHub: https://github.com/livecli/livecli
-  Issue tracker: https://github.com/livecli/livecli/issues
-  Download stable version: https://github.com/livecli/livecli/releases/latest
-  Stable Website: https://livecli.github.io/index.html
-  Latest Website: https://livecli.github.io/latest/index.html
-  PyPI: https://pypi.org/project/livecli/

Other versions

-  E2 receiver: https://livecli.github.io/latest/app_e2.html
-  Kodi: https://livecli.github.io/latest/app_kodi.html

Livecli is a fork of the
`Streamlink <https://github.com/streamlink/streamlink>`__ and
`Livestreamer <https://github.com/chrippa/livestreamer>`__ project

`Installation <https://livecli.github.io/install.html>`__
=========================================================

Installation via Python pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    pip install livecli

Manual installation via Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    git clone https://github.com/livecli/livecli
    cd livecli
    python setup.py install

Features
========

Livecli is built via a plugin system which allows new services to be
easily added.

A list of all supported plugins can be found on the `plugin
page <https://livecli.github.io/plugin_matrix.html>`__.

There is also a generic plugin that will try to open a stream on every website.

Quickstart
==========

After installing, simply use:

::

    livecli STREAMURL best

Livecli will automatically open the stream in its default video player!

See `Livecli's detailed
documentation <https://livecli.github.io/cli.html>`__ for all available
configuration options, CLI parameters and usage examples.

Contributing
============

All contributions are welcome. Feel free to open a new thread on the
issue tracker or submit a new pull request. Please read
`CONTRIBUTING.md <https://github.com/livecli/livecli/blob/master/CONTRIBUTING.md>`__
first. Thanks!

Please be aware that plugins for streaming services that are using DRM
protections, websites from not official or not authored third party
**will not be implemented**.

.. |TravisCI| image:: https://api.travis-ci.org/livecli/livecli.svg?branch=master
   :target: https://travis-ci.org/livecli/livecli
