# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibkit', 'bibkit.identifiers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bibkit',
    'version': '0.2.1',
    'description': 'A collection of tools for coding librarians and coders in libraries',
    'long_description': '# bibkit\n\n',
    'author': 'Daniel Opitz',
    'author_email': 'daniel@toilandtrouble.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/tt/bibkit',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
