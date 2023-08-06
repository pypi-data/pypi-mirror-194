# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_stimulus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-stimulus',
    'version': '0.2.0',
    'description': 'Use Hotwire Stimulus in your Django application.',
    'long_description': '',
    'author': 'Josiah Kaviani',
    'author_email': 'proofit404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
