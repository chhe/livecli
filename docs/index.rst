Overview
--------

Livecli is a :ref:`command-line utility <cli>` that pipes video streams
from various services into a video player, such as `VLC <http://videolan.org/>`_.

The main purpose of Livecli is to convert CPU-heavy websites to a
less CPU-intensive format.

There is also an :ref:`API <api_guide>` available for developers who want access
to the video stream data. This project is a fork of Streamlink and Livestreamer.

- Latest release: |version| (https://github.com/livecli/livecli/releases/latest)
- GitHub: https://github.com/livecli/livecli
- Issue tracker: https://github.com/livecli/livecli/issues
- PyPI: https://pypi.python.org/pypi/livecli
- Free software: Simplified BSD license

Features
--------

Livecli is built upon a plugin system which allows support for new services
to be easily added. Currently most of the big streaming services are supported,
such as:

- `Dailymotion <https://dailymotion.com/live>`_
- `Twitch <https://twitch.tv>`_
- `UStream <http://ustream.tv>`_
- `YouTube Live <https://youtube.com>`_

... and many more. A full list of plugins currently included can be found
on the :ref:`plugin_matrix` page.

There is also a generic plugin that will try to open a stream on every website.

Quickstart
----------

The default behaviour of Livecli is to playback a stream in the default
player (`VLC`_).

.. sourcecode:: console

    # pip install livecli
    $ livecli twitch.tv/twitch best
    [cli][info] Found matching plugin twitch for URL twitch.tv/twitch
    [cli][info] Opening stream: source (hls)
    [cli][info] Starting player: vlc

For more in-depth usage and install instructions see the `User guide`_.

User guide
----------

Livecli is made up of two parts, a :ref:`cli` and a library :ref:`API <api>`.
See their respective sections for more information on how to use them.

.. toctree::
    :maxdepth: 2

    install
    cli
    plugin_matrix
    players
    issues
    api_guide
    api
    changelog
    applications
