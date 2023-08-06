# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.26.4,<0.27.0']

setup_kwargs = {
    'name': 'rpaframework-openai',
    'version': '1.0.2',
    'description': 'OpenAI library for RPA Framework',
    'long_description': 'rpaframework-openai\n===================\n\nThis library enables OpenAI Services for `RPA Framework`_\nlibraries.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
