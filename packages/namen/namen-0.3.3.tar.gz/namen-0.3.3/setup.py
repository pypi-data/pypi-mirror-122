# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['namen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'namen',
    'version': '0.3.3',
    'description': '',
    'long_description': None,
    'author': 'Dennis van Bohemen',
    'author_email': 'dennis.van.bohemen@profit4cloud.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
