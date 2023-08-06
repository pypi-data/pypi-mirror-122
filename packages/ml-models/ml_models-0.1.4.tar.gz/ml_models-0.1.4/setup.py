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
['matplotlib>=3.4.3,<4.0.0', 'pandas>=1.3.3,<2.0.0', 'sklearn>=0.0,<0.1']

entry_points = \
{'console_scripts': ['app = ml_models.driver.main:main',
                     'cli = ml_models.console.console:main']}

setup_kwargs = {
    'name': 'ml-models',
    'version': '0.1.4',
    'description': ' This project is based upon basic ml-model testing and building a table.',
    'long_description': "This repository is stacked with the multiple ml models looped over certain times, \n\nThe User can install the ml_models and use the project as shown in driver package. \n\nThe data needs to be concise and at last you'll have a table generated over different ml models with different evaluation technique. With this you can directly check the model to use for.\n\n",
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
