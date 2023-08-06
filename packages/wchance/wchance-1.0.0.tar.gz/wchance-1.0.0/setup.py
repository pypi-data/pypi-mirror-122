# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wchance']
setup_kwargs = {
    'name': 'wchance',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'just4ius',
    'author_email': 'akravcuk808@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
