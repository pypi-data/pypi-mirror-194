# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['anycable']
setup_kwargs = {
    'name': 'anycable',
    'version': '0.2.0',
    'description': 'Polyglot replacement for Ruby WebSocket servers with Action Cable protocol',
    'long_description': '',
    'author': 'Josiah Kaviani',
    'author_email': 'proofit404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
}


setup(**setup_kwargs)
