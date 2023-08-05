# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reaktion',
 'reaktion.atoms',
 'reaktion.atoms.combination',
 'reaktion.atoms.transformation']

package_data = \
{'': ['*']}

install_requires = \
['fluss>=0.1.24', 'rekuest>=0.1.10']

setup_kwargs = {
    'name': 'reaktion',
    'version': '0.1.10',
    'description': '',
    'long_description': 'None',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
