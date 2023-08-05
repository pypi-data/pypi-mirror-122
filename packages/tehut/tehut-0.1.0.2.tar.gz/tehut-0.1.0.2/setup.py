# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tehut']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.10.0,<9.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tehut',
    'version': '0.1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Lennart Keller',
    'author_email': 'lennart.keller@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
