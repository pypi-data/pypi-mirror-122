# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['l18nprint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'l18nprint',
    'version': '0.1.0',
    'description': 'Python monkey patch wrapper for making print print correctly.',
    'long_description': None,
    'author': 'novafacing',
    'author_email': 'rowanbhart@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
