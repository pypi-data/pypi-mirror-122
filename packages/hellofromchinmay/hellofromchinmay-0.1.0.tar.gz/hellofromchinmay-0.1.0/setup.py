# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hellofromchinmay']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hellofromchinmay',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'chinmay',
    'author_email': 'bhagyesh.deshmukh29@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
