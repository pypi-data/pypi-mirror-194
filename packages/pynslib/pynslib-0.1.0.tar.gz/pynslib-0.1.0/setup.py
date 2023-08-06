# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynslib',
 'pynslib.async',
 'pynslib.async.modules',
 'pynslib.sync',
 'pynslib.sync.modules']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'pynslib',
    'version': '0.1.0',
    'description': 'A synchronous/asynchronous library for the NS API',
    'long_description': 'None',
    'author': 'Aav',
    'author_email': 'aav.verinhall@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AavHRF/nslib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
