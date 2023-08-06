# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_models',
 'ml_models.console',
 'ml_models.driver',
 'ml_models.hyper_parameter optimization']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'sklearn>=0.0,<0.1']

entry_points = \
{'console_scripts': ['app = ml_models.console.main:main',
                     'cli = ml_models.console.console:main']}

setup_kwargs = {
    'name': 'ml-models',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'addyR',
    'author_email': 'adarsharegmi121@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
