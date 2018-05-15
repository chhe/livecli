.. _plugin_matrix:


Plugins
=======

Overview
--------

This is a list of the currently built in plugins and what URLs and features
they support. Livecli's primary focus is live streams, so VOD support
is limited.

There is also a built in plugin that will try to open a stream on every website.

.. include:: _build/plugin_matrix.txt

Resolve Plugin
--------------

  The resolve plugin will try to open a stream on every website.

How does it work?
^^^^^^^^^^^^^^^^^
  It will try to find an embedded video url in the html sourcecode, |br|
  if there is no one it will try to find an embedded iframe url. |br|
  With the iframe url it will restart the script and do the same again |br|
  first it will search for a video url and after this for an iframe url.

Why does it not work?
^^^^^^^^^^^^^^^^^^^^^

  It will only work for streams that are viewable in the html sourcecode. |br|
  This plugin won't work for streams behind an API or some sort of encryption.

Wrong iframe selected?
^^^^^^^^^^^^^^^^^^^^^^
  When there are more than one iframe on the website, |br|
  Livecli will pick the url in alphabetically order.

  .. hint::

      Every removed or not used URL can be seen in the terminal
      with the :option:`--loglevel debug <--loglevel>` command.

How to ignore domains?
^^^^^^^^^^^^^^^^^^^^^^

  With this commands it can be ignored very easily, |br|
  you can add the ignored permanently in the :ref:`configuration file <cli-liveclirc>`

  - :option:`--resolve-blacklist-netloc NETLOC <--resolve-blacklist-netloc>`
  - :option:`--resolve-whitelist-netloc NETLOC <--resolve-whitelist-netloc>`

How to ignore domain paths?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

  Sometimes the websites have embedded url's from the same source, |br|
  but some won't contain valid video urls. |br|
  With this commands the wrong path can be ignored very easily, |br|
  you can add the ignored permanently in the :ref:`configuration file <cli-liveclirc>`

  - :option:`--resolve-blacklist-path PATH <--resolve-blacklist-path>`
  - :option:`--resolve-whitelist-path PATH <--resolve-whitelist-path>`

.. |br| raw:: html

    <br/>
