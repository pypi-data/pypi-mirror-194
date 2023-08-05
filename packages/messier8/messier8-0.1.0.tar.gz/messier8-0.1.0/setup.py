# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['messier8']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'messier8',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Daniel Konopka',
    'author_email': 'github@konopka.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
