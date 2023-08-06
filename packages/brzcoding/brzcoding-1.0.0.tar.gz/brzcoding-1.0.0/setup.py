# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brzcoding']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'brzcoding',
    'version': '1.0.0',
    'description': 'Programação simples, veloz e sem complicações',
    'long_description': None,
    'author': 'Gustavo Martinez',
    'author_email': 'gamezinhoo@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
