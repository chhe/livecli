.. _app_kodi:

:orphan:

**********
Kodi Guide
**********

  Livecli can be used as a **service proxy** for Kodi **IPTV Simple PVR**

  .. Attention::

      **script.module.pycryptodome** is required for Livecli,
      but it's only prepacked on **Kodi Leia**.

      If you want to use this Addon on **Krypton**, you will have to install **pycryptodome** on your system
      and create a *dummy* **script.module.pycryptodome** Addon.

Install Livecli
===============

   Download *repository.livecli*
   `(ZIP) <https://raw.githubusercontent.com/livecli/repo/master/repository.livecli/repository.livecli-2.0.0.zip>`_

   Install *service.livecli.proxy*

   .. Note:: A Kodi restart is recommended.

M3U URL
=======

  In order to access Livecli, you will have to create an url for **IPTV Simple PVR**

  For this Examples ``53473`` is used as the **default port**.

Basic URL
---------

  The basic url where Livecli will handle the playback looks like this.

  ::

    http://127.0.0.1:53473/play/?url=https://example.com/example

URL encoded
-----------

  The above solution will work for the most websites,
  but URLs with special characters such as ``?`` or ``&``
  might not work.

  For this case every parameter should be URL encoded,
  the website `urlencoder.org <https://www.urlencoder.org/>`_ can be used for this.

  ::

    http://127.0.0.1:53473/play/?url=https%3A%2F%2Fexample.com%2Fexample

Quality
-------

  By default Livecli will open the best quality,
  if you want a different quality you can use the parameter ``q``

  with every new parameter, you must add an ``&``

  For this example we will have the parameter ``url`` and ``q``

  ::

    http://127.0.0.1:53473/play/?url=URL&q=720p

Options
-------

  The **/play/** url can handle almoste every Livecli command.

  Example ``--hls-session-reload``

  some commands are different than in the normal Livecli version,
  for this command ``HH:MM:SS`` won't work here, you will have to use only ``seconds``

  This hls url will get a new session every 60 minutes (3600 seconds)

  ::

    http://127.0.0.1:53473/play/?url=URL&hls-session-reload=3600

Redirect
--------

  There is also a different version which only redirects the streaming url,

  only the basic parameter will work for this such as ``url`` and ``q``

  Livecli is only used to get the url, your Player will handle the playback.

  ::

    http://127.0.0.1:53473/301/?url=URL


Examples
========

  Here are some finished working examples.

  **Euronews**

  ::

    #EXTINF:-1 tvg-id="EURONEWS" group-title="English;News" tvg-logo="",Euronews
    http://127.0.0.1:53473/play/?url=https%253A%252F%252Fwww.euronews.com%252Flive

  **France24**

  ::

    #EXTINF:-1 tvg-id="France24" group-title="English;News" tvg-logo="",France24
    http://127.0.0.1:53473/play/?url=https%3A%2F%2Fwww.youtube.com%2Fuser%2Ffrance24

Python user
===========

  For people with python experience,
  there is also this `IPTV M3U Playlist Generator <https://github.com/livecli/iptv>`_

  It allows you to create a valid m3u file from a JSON formatted config file.
