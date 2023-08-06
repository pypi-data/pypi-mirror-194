# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peprock',
 'peprock._version',
 'peprock.datetime',
 'peprock.models',
 'peprock.subclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'peprock',
    'version': '0.4.0',
    'description': 'Foundational Python library',
    'long_description': '# peprock\nFoundational Python library\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)\n[![codecov](https://codecov.io/gh/Ponte-Energy-Partners/peprock/branch/main/graph/badge.svg?token=LWI96U2WSI)](https://codecov.io/gh/Ponte-Energy-Partners/peprock)\n[![test](https://github.com/Ponte-Energy-Partners/peprock/actions/workflows/test.yml/badge.svg)](https://github.com/Ponte-Energy-Partners/peprock/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/peprock.svg)](https://badge.fury.io/py/peprock)\n',
    'author': 'Jakob Keller',
    'author_email': '57402305+jakob-keller@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ponte-Energy-Partners/peprock',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
