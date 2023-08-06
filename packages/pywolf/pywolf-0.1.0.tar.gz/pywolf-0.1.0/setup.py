# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywolf', 'pywolf.db', 'pywolf.lang']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=23.0.0,<24.0.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'pywolf',
    'version': '0.1.0',
    'description': 'python utils',
    'long_description': None,
    'author': 'winglechen',
    'author_email': 'winglechen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
