# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['leap_model_rebuilder']
install_requires = \
['tensorflow>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'leap-model-rebuilder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
