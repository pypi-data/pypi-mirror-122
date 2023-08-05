# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tralalalal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tralalalal',
    'version': '1.0.0',
    'description': 'package from sda academy course with python tirana al 4',
    'long_description': None,
    'author': 'slikaj-jb',
    'author_email': 'sokol@jebbit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
