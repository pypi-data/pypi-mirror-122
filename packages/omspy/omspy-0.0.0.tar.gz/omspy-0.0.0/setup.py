# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omspy']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'omspy',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Ubermensch',
    'author_email': 'uberdeveloper001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
