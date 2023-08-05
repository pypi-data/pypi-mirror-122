# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shorthair']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shorthair',
    'version': '0.1.2',
    'description': 'Shorthair provides a way to access JSON object, it returns None rather than raising KeyError when key does not exist.',
    'long_description': None,
    'author': 'Aaron Zhang',
    'author_email': 'rabbit.aaron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
