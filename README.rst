############
github-stats
############

Just a simple script to help me enumerate LSST repositories I contributed to during FY2016 for my annual review.
Could it become something more?
*Absolutely.*

Installation
============

Python 3 only::

  git clone https://github.com/jonathansick/github-stats
  cd github-stats
  mkvirtualenv github-stats
  pip install -r requirements.txt

Usage
=====

::
  ./githubstats.py

You'll enter your GitHub username, password, and 2FA token (as necessary).

License
=======

Copyright 2017 Jonathan Sick
Copyright 2016-2017 Association of Universities for Research in Astronomy.

MIT licensed open source.

Uses code from https://github.com/lsst-sqre/sqre-codekit.
