# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goap',
 'goap.utils',
 'goap.utils.aws',
 'goap.utils.command',
 'goap.utils.commons',
 'goap.utils.gcp',
 'goap.utils.os']

package_data = \
{'': ['*']}

install_requires = \
['Automat==0.8.0', 'networkx==2.3', 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'goap',
    'version': '0.3.0',
    'description': 'Goal Oriented Action Planning alghorithm implementation in Python',
    'long_description': None,
    'author': 'Leonardo Pepe de Freitas',
    'author_email': 'lpepefreitas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
