# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dejawidth']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dejawidth',
    'version': '0.1.1',
    'description': 'measure the width, in pixels, of a string rendered using dejavu sans 110pt',
    'long_description': None,
    'author': 'Rahul Jha',
    'author_email': 'rj722@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
