# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlochinmay']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hello = hlochinmay.hlochinmay:hello']}

setup_kwargs = {
    'name': 'hlochinmay',
    'version': '0.1.2',
    'description': 'This package takes name of the user as an argurement in the hello function and then greets the user. from hlochinmay.hlochinmay import hello. hello(<name>)',
    'long_description': None,
    'author': 'chinmay',
    'author_email': 'bhagyesh.deshmukh29@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
