Meta Package Manager
====================

|release| |versions| |build| |docs| |coverage|

**What is Meta Package Manager?**

* It provides the ``mpm`` multi-platform CLI (Linux, macOS, Windows)
* ``mpm`` is like `yt-dlp <https://github.com/yt-dlp/yt-dlp>`_, but for package managers instead of videos
* ``mpm`` solves `XKCD #1654 (Universal Install Script) <https://xkcd.com/1654/>`_
* Because ``mpm`` try to wrap all other package managers, it became another pathological case of `XKCD #927 (Standards) <https://xkcd.com/927/>`_

.. |release| image:: https://img.shields.io/pypi/v/meta-package-manager.svg
    :target: https://pypi.python.org/pypi/meta-package-manager
    :alt: Last release
.. |versions| image:: https://img.shields.io/pypi/pyversions/meta-package-manager.svg
    :target: https://pypi.python.org/pypi/meta-package-manager
    :alt: Python versions
.. |build| image:: https://github.com/kdeldycke/meta-package-manager/workflows/Tests/badge.svg
    :target: https://github.com/kdeldycke/meta-package-manager/actions?query=workflow%3ATests
    :alt: Unittests status
.. |docs| image:: https://readthedocs.org/projects/meta-package-manager/badge/?version=develop
    :target: https://meta-package-manager.readthedocs.io/en/develop/
    :alt: Documentation Status
.. |coverage| image:: https://codecov.io/gh/kdeldycke/meta-package-manager/branch/develop/graph/badge.svg
    :target: https://codecov.io/github/kdeldycke/meta-package-manager?branch=develop
    :alt: Coverage Status

.. figure:: https://raw.githubusercontent.com/kdeldycke/meta-package-manager/develop/docs/mpm-managers-cli.png
    :align: center

.. figure:: https://raw.githubusercontent.com/kdeldycke/meta-package-manager/develop/docs/mpm-outdated-cli.png
    :align: center


Features
--------

* Inventory and list all package managers available on the system.
* Supports macOS, Linux and Windows.
* List installed packages.
* Search for packages.
* Install a package.
* List outdated packages.
* Sync local package infos.
* Upgrade all outdated packages.
* Backup list of installed packages to TOML file.
* Restore/install list of packages from TOML files.
* Pin-point commands to a subset of package managers (include/exclude
  selectors).
* Export results in JSON or user-friendly tables.
* Shell auto-completion for Bash, Zsh and Fish.
* Provides a `xbar plugin
  <https://meta-package-manager.readthedocs.io/en/develop/xbar.html>`_ for
  friendly macOS integration.


Supported package managers
--------------------------

================ ============= ====== ====== ======== ========= ============== ================ ============ ============= ============ ============
Package manager  Min. version  macOS  Linux  Windows  ``sync``  ``installed``  ``search``       ``install``  ``outdated``  ``upgrade``  ``cleanup``
================ ============= ====== ====== ======== ========= ============== ================ ============ ============= ============ ============
|apm|__           1.0.0         ✓      ✓      ✓                  ✓              ✓                 ✓           ✓             ✓
|apt|__           1.0.0                ✓               ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|apt-mint|__      1.0.0                ✓               ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|brew|__          2.7.0         ✓      ✓               ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|cask|__          2.7.0         ✓                      ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|choco|__         0.10.4                      ✓        ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|composer|__      1.4.0         ✓      ✓      ✓        ✓         ✓              ✓                 ✓           ✓             ✓            ✓
|flatpak|__       1.2.0                ✓                         ✓              ✓                 ✓           ✓             ✓            ✓
|gem|__           2.5.0         ✓      ✓      ✓                  ✓              ✓                 ✓           ✓             ✓            ✓
|mas|__           1.6.1         ✓                                ✓              ✓                 ✓           ✓             ✓
|npm|__           4.0.0         ✓      ✓      ✓                  ✓              ✓                 ✓           ✓             ✓
|opkg|__          0.2.0                ✓               ✓         ✓              ✓                 ✓           ✓             ✓
|pip|__           10.0.0        ✓      ✓      ✓                  ✓              |pip-search|__    ✓           ✓             ✓
|snap|__          2.0.0                ✓                         ✓              ✓                 ✓                         ✓
|vscode|__        1.60.0        ✓      ✓      ✓                  ✓              ✓                 ✓                         ✓
|yarn|__          1.21.0        ✓      ✓      ✓                  ✓              ✓                 ✓           ✓             ✓            ✓
================ ============= ====== ====== ======== ========= ============== ================ ============ ============= ============ ============

.. |apm| replace::
   Atom's ``apm``
__ https://atom.io/packages
.. |apt| replace::
   ``apt``
__ https://wiki.debian.org/Apt
.. |apt-mint| replace::
   Linux Mint's ``apt``
__ https://github.com/kdeldycke/meta-package-manager/issues/52
.. |brew| replace::
   Homebrew
__ https://brew.sh
.. |cask| replace::
   Homebrew Cask
__ https://caskroom.github.io
.. |choco| replace::
   Chocolatey
__ https://chocolatey.org
.. |composer| replace::
   ``composer``
__ https://getcomposer.org
.. |flatpak| replace::
   Flatpak
__ https://flatpak.org
.. |gem| replace::
   Ruby's ``gem``
__ https://rubygems.org
.. |mas| replace::
   Mac AppStore via ``mas``
__ https://github.com/argon/mas
.. |npm| replace::
   Node's ``npm``
__ https://www.npmjs.com
.. |opkg| replace::
   opkg
__ https://git.yoctoproject.org/cgit/cgit.cgi/opkg/
.. |pip| replace::
   Python ``pip``
__ https://pypi.org
.. |pip-search| replace::
   ✘*
__ https://github.com/pypa/pip/issues/5216#issuecomment-744605466
.. |snap| replace::
   ``snap``
__ https://snapcraft.io
.. |vscode| replace::
   Visual Studio Code
__ https://code.visualstudio.com
.. |yarn| replace::
   Node's ``yarn``
__ https://yarnpkg.com


If you're bored, feel free to add support for new package manager. See
good candidates at:

* `Wikipedia list of package managers
  <https://en.wikipedia.org/wiki/List_of_software_package_management_systems>`_
* `Awesome list of package managers
  <https://github.com/k4m4/terminals-are-sexy#package-managers>`_
* `GitHub list of package managers
  <https://github.com/showcases/package-managers>`_


Installation
------------

This package is `available on PyPi
<https://pypi.python.org/pypi/meta-package-manager>`_, so you can install the
latest stable release and its dependencies with a simple ``pip`` call:

.. code-block:: shell-session

    $ pip install meta-package-manager


Documentation
-------------

Docs are `hosted on Read the Docs
<https://meta-package-manager.readthedocs.io>`_.


Usage
-----

Examples of the package's ``mpm`` CLI.

List global options and commands:

.. code-block:: shell-session

    $ mpm
    Usage: mpm [OPTIONS] COMMAND [ARGS]...

      CLI for multi-package manager upgrades.

    Options:
      -m, --manager [composer|snap|brew|cask|mas|vscode|npm|yarn|apm|apt|apt-mint|flatpak|pip|gem|opkg|choco]
                                      Restrict sub-command to a subset of package
                                      managers. Repeat to select multiple
                                      managers.  [default: ]
      -e, --exclude [composer|snap|brew|cask|mas|vscode|npm|yarn|apm|apt|apt-mint|flatpak|pip|gem|opkg|choco]
                                      Exclude a package manager. Repeat to exclude
                                      multiple managers.  [default: ]
      -a, --all-managers              Force evaluation of all package manager
                                      implemented by mpm, even those notsupported
                                      by the current platform. Still applies
                                      filtering by --manager and --exclude options
                                      before calling the subcommand.  [default:
                                      False]
      --ignore-auto-updates / --include-auto-updates
                                      Report all outdated packages, including
                                      those tagged as auto-updating. Only applies
                                      to 'outdated' and 'upgrade' commands.
                                      [default: ignore-auto-updates]
      -o, --output-format [ascii|csv|csv-tab|double|fancy_grid|github|grid|html|jira|json|latex|latex_booktabs|mediawiki|minimal|moinmoin|orgtbl|pipe|plain|psql|psql_unicode|rst|simple|textile|tsv|vertical]
                                      Rendering mode of the output.  [default:
                                      psql_unicode]
      -s, --sort-by [manager_id|package_name|package_id|manager_name|version]
                                      Sort results.  [default: manager_id]
      --stats / --no-stats            Print per-manager package statistics.
                                      [default: stats]
      --time / --no-time              Measure and print elapsed execution time.
                                      [default: no-time]
      --stop-on-error / --continue-on-error
                                      Stop right away or continue operations on
                                      manager CLI error.  [default: continue-on-
                                      error]
      -d, --dry-run                   Do not actually perform any action, just
                                      simulate CLI calls.  [default: False]
      -C, --config CONFIG_PATH        Location of the configuration file.
      -v, --verbosity LEVEL           Either CRITICAL, ERROR, WARNING, INFO or
                                      DEBUG.  [default: INFO]
      --version                       Show the version and exit.  [default: False]
      -h, --help                      Show this message and exit.  [default:
                                      False]

    Commands:
      backup     Save installed packages to a TOML file.
      cleanup    Cleanup local data.
      install    Install a package.
      installed  List installed packages.
      managers   List supported package managers and their location.
      outdated   List outdated packages.
      restore    Install packages in batch as specified by TOML files.
      search     Search packages.
      sync       Sync local package info.
      upgrade    Upgrade all packages.

List all supported package managers and their status on current system (macOS):

.. code-block:: shell-session

    $ mpm -a managers
    ┌────────────────────┬──────────┬─────────────────┬────────────────────────────┬────────────┬───────────┐
    │ Package manager    │ ID       │ Supported       │ CLI                        │ Executable │ Version   │
    ├────────────────────┼──────────┼─────────────────┼────────────────────────────┼────────────┼───────────┤
    │ Atom's apm         │ apm      │ ✓               │ ✓  /usr/local/bin/apm      │ ✓          │ ✓  2.6.2  │
    │ APT                │ apt      │ ✘  Linux only   │ ✓  /usr/bin/apt            │ ✓          │ ✘         │
    │ Linux Mint's apt   │ apt-mint │ ✘  Linux only   │ ✓  /usr/bin/apt            │ ✓          │ ✘         │
    │ Homebrew Formulae  │ brew     │ ✓               │ ✓  /usr/local/bin/brew     │ ✓          │ ✓  3.2.13 │
    │ Homebrew Cask      │ cask     │ ✓               │ ✓  /usr/local/bin/brew     │ ✓          │ ✓  3.2.13 │
    │ Chocolatey         │ choco    │ ✘  Windows only │ ✘  choco not found         │            │           │
    │ PHP's Composer     │ composer │ ✓               │ ✓  /usr/local/bin/composer │ ✓          │ ✓  2.1.8  │
    │ Flatpak            │ flatpak  │ ✘  Linux only   │ ✘  flatpak not found       │            │           │
    │ Ruby Gems          │ gem      │ ✓               │ ✓  /usr/bin/gem            │ ✓          │ ✓  3.0.3  │
    │ Mac AppStore       │ mas      │ ✓               │ ✓  /usr/local/bin/mas      │ ✓          │ ✓  1.8.3  │
    │ Node's npm         │ npm      │ ✓               │ ✓  /usr/local/bin/npm      │ ✓          │ ✓  7.24.0 │
    │ OPKG               │ opkg     │ ✘  Linux only   │ ✘  opkg not found          │            │           │
    │ Pip                │ pip      │ ✓               │ ✓  /usr/local/bin/python3  │ ✓          │ ✓  21.2.4 │
    │ Snap               │ snap     │ ✘  Linux only   │ ✘  snap not found          │            │           │
    │ Visual Studio Code │ vscode   │ ✓               │ ✓  /usr/local/bin/code     │ ✓          │ ✓  1.60.2 │
    │ Node's yarn        │ yarn     │ ✓               │ ✘  yarn not found          │            │           │
    └────────────────────┴──────────┴─────────────────┴────────────────────────────┴────────────┴───────────┘
