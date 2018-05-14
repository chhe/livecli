.. _app_e2:

:orphan:

.. |PATH| raw:: html

    https://raw.githubusercontent.com/livecli/ipk/master/build/

.. |br| raw:: html

    <br/>

*****************
E2 receiver Guide
*****************

  The E2 version will run the command ``livecli --server --server-host 0.0.0.0 -l debug`` |br|
  which can be used for local testing without the receiver.

  The source and build files can be found at https://github.com/livecli/ipk

  .. attention::

    This is only tested with a **Vu+ Duo2** |br|
    which is an E2 receiver with *init.d* and *python2.7*

Install Livecli
===============

opkg files
----------

  At the begin you will install the packages from ``opkg``

  .. code-block:: bash

    opkg install python-futures
    opkg install python-singledispatch
    opkg install python-six
    opkg install python-requests

  .. note::

    **python-pycrypto** was preinstalled on my test receiver,
    you might need to install it on your.
    |br| |br|
    If this is not posible you can try
    **python-pycryptodome** or **python-pycryptodomex**

download files
--------------

  You will have to download all required files, |br|
  for this example all the files will be saved in ``/tmp``

  The best way is to use the terminal, |br|
  from the terminal you can use ``wget URL`` to download the files |br|
  and ``cd /tmp`` to get into the example direction.

  All these files are required.

  - \ |PATH|\ python-backports.shutil-get-terminal-size_1.0.0_all.ipk
  - \ |PATH|\ python-backports.shutil-which_3.5.1_all.ipk
  - \ |PATH|\ python-iso3166_0.8_all.ipk
  - \ |PATH|\ python-iso639_0.4.5_all.ipk
  - \ |PATH|\ python-socks_1.6.8_all.ipk
  - \ |PATH|\ python-websocket_0.47.0_all.ipk
  - \ |PATH|\ python-livecli\_\ |version|\ _all.ipk

install
-------

  For the install after the download,
  you will have to use ``opkg install PATH_IPK``

  .. note::

    Install python-livecli\_\ |version|\ _all.ipk as the last package

  .. hint::

    You can use the **TAB** key, to autocomplete names |br| |br|
    *opkg install /tmp/py* |br|
    **TAB** will be *opkg install /tmp/python-* |br| |br|
    *opkg install /tmp/python-so* |br|
    **TAB** will be *opkg install /tmp/python-socks_1.6.8_all.ipk*

after install
-------------

  You can test your Livecli installation in your terminal.

  Type

  ::

    livecli -l debug

  it should output some information about Livecli and your system.

service
-------

  Now that Livecli works, you will have to install the service script.

  .. note::

      This will only work for receiver with *init.d*

  **download**

    - \ |PATH|\ enigma2-livecli-server_1.0.0_all.ipk

  **install**

    ::

      opkg install /tmp/enigma2-livecli-server_1.0.0_all.ipk

  **start the server**

    ::

      update-rc.d /etc/init.d/livecli-server defaults

Known issues
============

SystemTimeWarning
-----------------

  This issue comes up if your receiver starts without a satellite signal.

  ::

    /usr/lib/python2.7/site-packages/requests/packages/urllib3/connection.py:303:
    SystemTimeWarning: System time is way off (before 2014-01-01).
    This will probably lead to SSL verification errors SystemTimeWarning

  To solve this, you need to install **Network Time Protocol (NTP)** service

  After the install you might need to run

  ::

    update-rc.d /etc/init.d/ntpupdate.sh defaults

Userbouquet
===========

  In order to access Livecli, you will have to create a valid url.

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

Colon
-----

  .. attention::

    Because this is used for the Userbouquet **:** is not allowed in the URL, |br|
    you will have to replace **:** with **%3a**

  **Before**

  ::

    http://127.0.0.1:53473/play/?url=URL

  **After**

  ::

    http%3a//127.0.0.1%3a53473/play/?url=URL

Service id
----------

  If you use the webinterface, you can just copy your finished URL there. |br|
  But if you use a text editor, you will have to create a valid Userbouquet.

  I will use the service id **4097** IPTV for my examples.

  You can use a different service id such as

  - service **5001** gstplayer (gstreamer)
  - service **5002** exteplayer3 (ffmpeg)

  You might need to install a serviceapp for **5001** and **5002**

  ::

    opkg install enigma2-plugin-systemplugins-serviceapp

  .. note::

      But I only tested it with **4097**

Examples
========

  Here are some finished working examples.

  **Euronews**

  ::

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53473/play/?url=https%253A%252F%252Fwww.euronews.com%252Flive:Euronews
    #DESCRIPTION Euronews

  **France24**

  ::

    #SERVICE 4097:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a53473/play/?url=https%3A%2F%2Fwww.youtube.com%2Fuser%2Ffrance24:France24
    #DESCRIPTION France24
