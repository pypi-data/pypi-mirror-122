# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['adacord = cli.main:app']}

setup_kwargs = {
    'name': 'adacord-cli',
    'version': '0.1.1',
    'description': 'Adacord CLI',
    'long_description': None,
    'author': 'Christian Barra',
    'author_email': 'me@christianbarra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
