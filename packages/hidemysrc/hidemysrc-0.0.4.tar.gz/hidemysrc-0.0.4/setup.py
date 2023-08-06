# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hidemysrc']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'numpy>=1.22.2,<2.0.0',
 'pycryptodome>=3.17,<4.0',
 'replit>=3.2.4,<4.0.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'hidemysrc',
    'version': '0.0.4',
    'description': 'Python-based package for encrypting your python source code!',
    'long_description': None,
    'author': 'ecriminals',
    'author_email': 'bio@fbi.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
