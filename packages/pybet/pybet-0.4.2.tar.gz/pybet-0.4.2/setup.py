# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybet', 'pybet.staking']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybet',
    'version': '0.4.2',
    'description': 'A library of betting utilities to assist with calculation of bets, stakes and markets',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/pybet.svg?style=for-the-badge)](https://pypi.org/project/pybet/)\n[![docs: passing](https://readthedocs.org/projects/tabletoppy/badge/?version=latest)](https://pybet.readthedocs.io/en/latest/?badge=latest)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# pybet\n\npybet is a library of betting utilities to assist with calculation of bets, stakes and markets\n\n## Installation\n\n`pip install pybet`\n\nor\n\n`poetry add pybet`\n',
    'author': 'Robert Peacock',
    'author_email': 'robertjamespeacock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/peaky76/pybet',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
