# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_test_database']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0']

setup_kwargs = {
    'name': 'fast-test-database',
    'version': '0.1.0',
    'description': 'Configure an in-memory database for running Django tests',
    'long_description': None,
    'author': 'Alexey Kotlyarov',
    'author_email': 'a@koterpillar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
