# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ausbills', 'ausbills.parliament', 'ausbills.util']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'bs4>=0.0.1,<0.0.2',
 'flake8>=3.9.2,<4.0.0',
 'lxml>=4.6.3,<5.0.0',
 'pytest>=6.2.4,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'setuptools>=57.0.0,<58.0.0',
 'urlpath>=1.1.7,<2.0.0']

setup_kwargs = {
    'name': 'ausbills',
    'version': '1.0.0',
    'description': 'Get current parliament bills from Australian governments.',
    'long_description': None,
    'author': 'OpenGov Australia',
    'author_email': 'kip.crossing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
