# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibkit', 'bibkit.identifiers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bibkit',
    'version': '0.2.2',
    'description': 'A collection of tools for coding librarians and coders in libraries',
    'long_description': "# bibkit\n`bibkit` aims to be a toolkit for working with library metadata. It is still very young project and I develop it in my free time to learn about proper development of Python libraries and open source project maintainership. A more specific information and documentation will follow soon.\n\nI'll try to have a significant test coverage and in the near future I'll start testing against all supported Python versions ([https://devguide.python.org/versions/#versions](https://devguide.python.org/versions/#versions)). I skipped 3.7 because it won't be supported anymore in a few months. Unsupported Python versions will be dropped as soon as possible.\n\n## Installation\nTo install `bibkit` run `pip install bibkit`.",
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
