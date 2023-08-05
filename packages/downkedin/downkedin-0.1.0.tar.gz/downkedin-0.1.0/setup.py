# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['downkedin']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.7.4,<4.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'downkedin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tiagovla',
    'author_email': 'tiagovla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
