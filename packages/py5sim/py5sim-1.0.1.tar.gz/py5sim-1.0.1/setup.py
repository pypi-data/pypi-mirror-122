# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py5sim']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py5sim',
    'version': '1.0.1',
    'description': 'Easy package for 5sim.net api',
    'long_description': None,
    'author': 'abuztrade',
    'author_email': 'abuztrade.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
