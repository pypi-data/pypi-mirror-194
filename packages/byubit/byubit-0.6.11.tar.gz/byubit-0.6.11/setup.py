# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['byubit']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.0,<2.0.0']

setup_kwargs = {
    'name': 'byubit',
    'version': '0.6.11',
    'description': 'A library for teaching beginners how to program',
    'long_description': None,
    'author': 'Gordon Bean',
    'author_email': 'gbean@cs.byu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
