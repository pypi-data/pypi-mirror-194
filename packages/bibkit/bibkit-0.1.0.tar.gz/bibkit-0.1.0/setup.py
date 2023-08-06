# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibkit']

package_data = \
{'': ['*']}

install_requires = \
['ftfy>=6.1.1,<7.0.0']

setup_kwargs = {
    'name': 'bibkit',
    'version': '0.1.0',
    'description': 'A collection of tools for coding librarians and coders in libraries',
    'long_description': '# bibkit\n\n',
    'author': 'Daniel Opitz',
    'author_email': 'daniel@toilandtrouble.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
