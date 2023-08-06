# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guava_preconditions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'guava-preconditions',
    'version': '0.1.0',
    'description': "A python version of guava's preconditions",
    'long_description': None,
    'author': 'Elliana',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
