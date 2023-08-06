# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poutyne_transformers']

package_data = \
{'': ['*']}

install_requires = \
['Poutyne>=1.6,<2.0', 'torch>=1.9.0,<2.0.0', 'transformers>=4.11.3,<5.0.0']

setup_kwargs = {
    'name': 'poutyne-transformers',
    'version': '0.1.0',
    'description': 'Train 🤗-transformers models with Poutyne.',
    'long_description': None,
    'author': 'Lennart Keller',
    'author_email': 'lennart.keller@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
