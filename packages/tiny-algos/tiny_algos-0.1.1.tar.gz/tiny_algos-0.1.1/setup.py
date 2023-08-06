# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_algos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tiny-algos',
    'version': '0.1.1',
    'description': 'A compact modules for Data Structures and Algorithms',
    'long_description': None,
    'author': 'azriel1rf',
    'author_email': 'azriel.1rf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
