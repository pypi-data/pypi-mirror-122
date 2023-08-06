# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dadfes', 'tests', 'tests.app']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-admin-data-from-external-service',
    'version': '0.1.0',
    'description': 'Helpers to extend Django admin with data from external service with minimal hacks',
    'long_description': '',
    'author': 'Evgeniy Tatarkin',
    'author_email': 'tatarkin.evg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/estin/django-admin-data-from-external-service',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
