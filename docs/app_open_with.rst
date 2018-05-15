.. _app_open_with:

:orphan:

Open With Installation Guide
============================

Open With is a Browser extension

It allows you to open Livecli streams from your Browser.


1. Install Open With
--------------------

  - `Firefox <https://addons.mozilla.org/en-US/firefox/addon/open-with/>`_
  - `Chrome <https://chrome.google.com/webstore/detail/open-with/cogjlncmljjnjpbgppagklanlcbchlno>`_

2. Install the required .py file
--------------------------------

  For the install you will have to save a **.py** file
  and run the install command.

  Download the ``open_with_linux.py`` or ``open_with_windows.py`` file,

  which can be found in your **Open With** settings

  **Linux**

  open the path where you saved the **.py** file in your terminal.

  ::

    chmod u+x open_with_linux.py
    ./open_with_linux.py install

  **Windows**

  **You don't need to install Python**, you can use the packed version from Livecli.

  Change the path, if you saved it somewhere else.

  Run this command in your **cmd**

  ::

    "C:\Program Files (x86)\Livecli\Python\python" "C:\file\open_with_windows.py" install

3. Test Installation
--------------------

  click on *Test Installation*

4. Add Livecli
--------------

  click on *Add browser*

  **Name:** Livecli

  **Icon:** You can add Custom icons

  Download one of these

  - `<https://avatars0.githubusercontent.com/u/35533657>`_
  - `<https://avatars2.githubusercontent.com/u/24879726>`_

  Make sure to click on the Icon after you added it.

  **Command:** Add one of the following commands

Windows
^^^^^^^

  ::

    livecli "%s" best

Linux
^^^^^

  You will have to find the Livecli path

  Type ``which livecli`` for this example it will be ``/usr/local/bin/livecli``

  ::

    /usr/local/bin/livecli "%s" best

Linux with gnome-terminal
^^^^^^^^^^^^^^^^^^^^^^^^^

  You will have to find the Livecli and your terminal path

  Type ``which gnome-terminal`` for this example it will be ``/usr/bin/gnome-terminal``

  ::

    /usr/bin/gnome-terminal -- bash -c "/usr/local/bin/livecli \"%s\" best"

Linux with --player-passthrough
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ::

      /usr/bin/gnome-terminal -- bash -c "/usr/local/bin/livecli \"%s\" best --player-passthrough \"hls\""
