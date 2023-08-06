# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['first_poet_lib']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.20.0']

setup_kwargs = {
    'name': 'first-poet-lib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jagadeesh32',
    'author_email': 'katla.jagadeesh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
