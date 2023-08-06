# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioweb3']

package_data = \
{'': ['*']}

install_requires = \
['web3==5.24.0']

setup_kwargs = {
    'name': 'aioweb3',
    'version': '0.1.0',
    'description': 'asyncio web3 provider',
    'long_description': None,
    'author': 'Omar Bohsali',
    'author_email': 'omar.bohsali@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
