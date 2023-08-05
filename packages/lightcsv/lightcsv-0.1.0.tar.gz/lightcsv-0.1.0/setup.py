# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lightcsv']
setup_kwargs = {
    'name': 'lightcsv',
    'version': '0.1.0',
    'description': 'Simple pure Python CSV parser',
    'long_description': None,
    'author': 'Jose Rodriguez',
    'author_email': 'boriel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
