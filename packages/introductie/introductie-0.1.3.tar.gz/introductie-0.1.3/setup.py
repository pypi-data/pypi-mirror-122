# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['introductie']

package_data = \
{'': ['*']}

install_requires = \
['namen>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'introductie',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Dennis van Bohemen',
    'author_email': 'Dennis.Van.Bohemen@topicus.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
