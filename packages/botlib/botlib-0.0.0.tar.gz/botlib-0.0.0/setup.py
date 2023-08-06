# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'botlib',
    'version': '0.0.0',
    'description': '',
    'long_description': '',
    'author': 'Nikita Konodyuk',
    'author_email': 'konodyuk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
