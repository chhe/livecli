.. _install:

.. |br| raw:: html

  <br />

Installation
============

Source code
-----------

If a package is not available for your platform (or it's out of date) you
can install Livecli via source.

There are a few different methods to do this,
`pip <https://pip.readthedocs.io/en/latest/installing/>`_ the Python package
manager, or by checking out the latest code with
`Git <https://git-scm.com/downloads>`_.

.. note::

    For some Linux distributions the Python headers package needs to be installed before installing livecli
    (``python-devel`` in RedHat, Fedora, etc.).

    Ensure that you are using an up-to-date version of :command:`pip`, at least version **6** is recommended.


The commands listed here will also upgrade any existing version of Livecli.

==================================== ===========================================
Version                              Installing
==================================== ===========================================
`Latest release (pip)`_              .. code-block:: console

                                        # pip install livecli
`Development version (pip)`_         .. code-block:: console

                                        # pip install -U git+https://github.com/livecli/livecli.git

`Development version (git)`_         .. code-block:: console

                                        $ git clone git+https://github.com/livecli/livecli.git
                                        $ cd livecli
                                        # pip install -U .
==================================== ===========================================

.. _Latest release (pip): https://pypi.python.org/pypi/livecli
.. _Development version (pip): https://github.com/livecli/livecli
.. _Development version (git): https://github.com/livecli/livecli

Dependencies
^^^^^^^^^^^^

To install Livecli from source you will need these dependencies.

==================================== ===========================================
Name                                 Notes
==================================== ===========================================
`Python`_                            At least version **2.7** or **3.4**.
`python-setuptools`_

**Automatically installed by the setup script**
--------------------------------------------------------------------------------
`iso-639`_                           Used for localization settings, provides language information
`iso3166`_                           Used for localization settings, provides country information
`pycryptodome`_                      Required to play some encrypted streams
`pysocks`_
`python-futures`_                    Only needed on Python **2.x**.
`python-requests`_                   At least version **2.2**.
`python-singledispatch`_             Only needed on Python versions older than **3.4**.
`websocket`_

**Optional**
--------------------------------------------------------------------------------
`RTMPDump`_                          Required to play RTMP streams.
`ffmpeg`_                            Required to play streams that are made up of separate
                                     audio and video streams, eg. YouTube 1080p+
==================================== ===========================================

Using pycrypto and pycountry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With these environment variables it is possible to use

`pycrypto`_ or `pycryptodomex`_ instead of `pycryptodome`_

.. code-block:: console

    $ export LIVECLI_USE_PYCRYPTO="true"
    $ export LIVECLI_USE_PYCRYPTODOMEX="true"

`pycountry`_ instead of `iso-639`_ and `iso3166`_

.. code-block:: console

    $ export LIVECLI_USE_PYCOUNTRY="true"

.. _Python: http://python.org/
.. _python-setuptools: http://pypi.python.org/pypi/setuptools
.. _python-futures: http://pypi.python.org/pypi/futures
.. _python-requests: http://python-requests.org/
.. _python-singledispatch: http://pypi.python.org/pypi/singledispatch
.. _RTMPDump: http://rtmpdump.mplayerhq.hu/
.. _pycountry: https://pypi.python.org/pypi/pycountry
.. _pycrypto: https://www.dlitz.net/software/pycrypto/
.. _pycryptodome: https://pycryptodome.readthedocs.io/en/latest/
.. _pycryptodomex: https://pycryptodome.readthedocs.io/en/latest/src/introduction.html?highlight=pycryptodomex
.. _pysocks: https://pypi.python.org/pypi/PySocks
.. _websocket: https://pypi.python.org/pypi/websocket-client
.. _ffmpeg: https://www.ffmpeg.org/
.. _iso-639: https://pypi.python.org/pypi/iso-639
.. _iso3166: https://pypi.python.org/pypi/iso3166


Installing within a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not wish to install Livecli globally on your system it's
recommended to use `venv`_ to create a user owned Python environment
instead.

.. code-block:: console

    Creating an environment
    $ python3 -m venv ~/myenv

    Activating the environment
    $ source ~/myenv/bin/activate

    Installing livecli into the environment
    (myenv)$ pip install livecli

    Using livecli in the environment
    (myenv)$ livecli ...

    Deactivating the environment
    (myenv)$ deactivate

    Using livecli without activating the environment
    $ ~/myenv/bin/livecli ...


.. _venv: https://docs.python.org/3/library/venv.html


Windows binaries
----------------

==================================== ====================================
Release                              Notes
==================================== ====================================
`Stable release`_                    Download the installer from the `GitHub releases page`_.
==================================== ====================================

.. _Stable release:
.. _GitHub releases page: https://github.com/livecli/livecli/releases/latest

These installers contain:

- A compiled version of Livecli that **does not require an existing Python
  installation**
- `RTMPDump`_ for viewing RTMP streams
- `ffmpeg`_ for muxing streams

and perform the following tasks:

- Add Livecli to the system's list of installed applications. |br|
  An uninstaller will automatically be created during installation.
- Add Livecli's installation directory to the system's ``PATH`` environment variable. |br|
  This allows the user to run the ``livecli`` command globally
  from the command prompt or powershell without specifying its directory.

To build the installer on your own, ``NSIS`` and ``pynsist`` need to be installed.
