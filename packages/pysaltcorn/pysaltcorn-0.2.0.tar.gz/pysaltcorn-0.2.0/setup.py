# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysaltcorn']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pysaltcorn',
    'version': '0.2.0',
    'description': 'Python library for Saltcorn API',
    'long_description': None,
    'author': 'Michael Dubner',
    'author_email': 'pywebmail@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
