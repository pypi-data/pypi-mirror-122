# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['athame']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0', 'py-buzz>=2.1.3,<3.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'athame',
    'version': '0.1.0',
    'description': 'A tool for scheduling allowed/forbidden blocks of execution time for daemon processes.',
    'long_description': None,
    'author': 'Graham Drakeley',
    'author_email': 'gt.drakeley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
