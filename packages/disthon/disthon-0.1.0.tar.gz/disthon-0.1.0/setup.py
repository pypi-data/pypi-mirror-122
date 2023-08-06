# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disthon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'disthon',
    'version': '0.1.0',
    'description': 'A Discord API wrapper',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
