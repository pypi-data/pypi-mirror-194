# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drivesecrets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'drivesecrets',
    'version': '1.0.0',
    'description': 'Save secrets in your google drive to secure your Colaboratory notebooks.',
    'long_description': 'None',
    'author': 'Kevin Katz',
    'author_email': 'contact@kevinkatz.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
