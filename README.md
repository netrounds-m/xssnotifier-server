XSS Notifier
============

[![Build Status](https://api.travis-ci.org/mattiaslundberg/xssnotifier-server.png?branch=master)](https://travis-ci.org/mattiaslundberg/xssnotifier-server)
[![Coverage Status](https://coveralls.io/repos/mattiaslundberg/xssnotifier-server/badge.svg?branch=master&service=github)](https://coveralls.io/github/mattiaslundberg/xssnotifier-server?branch=master)

XSS notifier is a tool intended to help developers find XSS injections in web applications.



RUNNING (DEV)
=============

_First run_
 * Install python (3.x)
 * Install python virtualenv
 * Generate virtualenv `virtualenv --no-site-packages venv`

_Every run_
 * Activate virtualenv `source venv/bin/activate`

_Unittests_
 * `py.test tests`

_Running_
 * `python xssnotifier/main.py`



CONTRIBUTING
============
Any pull request aiming to improve the project is encouraged.

Make sure you follow [pep8](https://www.python.org/dev/peps/pep-0008/) style and add relevant test before submitting the pull request.



TODO
====

- [x] Send complete information to ws clients
- [X] Improve unittesting coverage
- [ ] Add integration tests
- [ ] Add storage for events (Database)
- [ ] Add user managing (register/login)
- [ ] Subscribe for specific user only
- [ ] Allow sharing results to other users
