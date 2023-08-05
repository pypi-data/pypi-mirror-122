# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_fabdb', 'tap_fabdb.tests']

package_data = \
{'': ['*']}

install_requires = \
['singer-sdk>=0.3.6,<0.4.0']

entry_points = \
{'console_scripts': ['tap-fabdb = tap_fabdb.tap:TapFabDb.cli']}

setup_kwargs = {
    'name': 'tap-fabdb',
    'version': '0.0.1',
    'description': 'A Singer tap for extracting data from the FaB DB API, built with the Singer SDK.',
    'long_description': '<p align="center">\n    <em>tap-fabdb, a Singer tap for extracting data from the <a href="https://fabdb.net/resources/api" target="_blank">FaB DB API</a>.</em>\n</p>\n<p align="center">\n  <a href="https://github.com/dwallace0723/tap-fabdb/actions">\n    <img src="https://github.com/dwallace0723/tap-fabdb/actions/workflows/test.yml/badge.svg"  alt="GitHub Actions" />\n  </a>\n  <a href="https://github.com/dwallace0723/tap-fabdb/actions">\n    <img src="https://github.com/dwallace0723/tap-fabdb/actions/workflows/release.yml/badge.svg"  alt="GitHub Actions" />\n  </a>\n  <a href="https://github.com/dwallace0723/tap-fabdb/actions">\n    <img src="https://github.com/dwallace0723/tap-fabdb/actions/workflows/publish.yml/badge.svg"  alt="GitHub Actions" />\n  </a>\n  <a href="https://codeclimate.com/github/dwallace0723/tap-fabdb/maintainability">\n    <img src="https://api.codeclimate.com/v1/badges/875607d70a6dc02a82df/maintainability" />\n  </a>\n  <a href="https://codeclimate.com/github/dwallace0723/tap-fabdb/test_coverage">\n    <img src="https://api.codeclimate.com/v1/badges/875607d70a6dc02a82df/test_coverage" />\n  </a>\n  <a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"  alt="Black" />\n  </a>\n</p>',
    'author': 'David Wallace',
    'author_email': 'david.wallace@dutchie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
