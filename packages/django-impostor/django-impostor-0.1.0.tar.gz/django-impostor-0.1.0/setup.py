# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_impostor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-impostor',
    'version': '0.1.0',
    'description': 'Pretend to be someone else, if you are a superuser, in Django',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@withlogic.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
