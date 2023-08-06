# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konbini', 'konbini.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'duckdb>=0.7.0,<0.8.0',
 'ibis>=3.2.0,<4.0.0',
 'pyarrow>=11.0.0,<12.0.0',
 'sqlglot>=11.2.3,<12.0.0']

entry_points = \
{'console_scripts': ['kon = konbini.cli.kon:kon']}

setup_kwargs = {
    'name': 'konbini',
    'version': '0.1.0',
    'description': 'Analytics one-stop shop, open 24/7',
    'long_description': '<br/>\n<div align="center">\n    <img src="assets/logo.svg" height="150px" />\n</div>\n\n# Konbini\nAn intelligent analytics store, open 24/7. Konbini unifies different data management frameworks to power fast and accurate analytic workloads at any scale.\n\n# Documentation\nAwaiting soft opening.\n\n# Installation\nThe package can be installed from PyPi with the following command:\n```\npip install konbini\n```\n\n# Contributions\nWe always welcome contributions! Please read our [guide](https://github.com/hyperplane-data/konbini/CONTRIBUTING.md) to get started.\n',
    'author': 'Hyperplane',
    'author_email': 'hyperplane.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hyperplane-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
