# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioxmlrpc', 'aioxmlrpc.tests']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aioxmlrpc',
    'version': '0.6.0',
    'description': 'Source code of Sequoia API TLDPublic',
    'long_description': None,
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/aioxmlrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
