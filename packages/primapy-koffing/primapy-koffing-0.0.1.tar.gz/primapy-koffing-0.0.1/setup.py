# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['primapy_koffing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-koffing',
    'version': '0.0.1',
    'description': 'Safety placeholder',
    'long_description': None,
    'author': 'AMOps',
    'author_email': 'amops@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
