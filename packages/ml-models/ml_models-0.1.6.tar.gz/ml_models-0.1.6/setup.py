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
    'version': '0.1.6',
    'description': ' This project is based upon basic ml-model testing and building a table.',
    'long_description': 'This repository is stacked with the multiple ml models looped over certain times, \n\nThe User can install the ml_models and use the project as shown in driver package. \n\nThe data needs to be concise and at last you\'ll have a table generated over different ml models with different evaluation technique. With this you can directly check the model to use for.\n\nfrom ml_models import *\nfrom ml_models.build_model import build_table\n\nrandom_forest_classifier= RandomForestClassifier(n_estimators= 10, criterion="entropy")  \n\n# for decision Tree\n# Create Decision Tree classifer object\ndecision_tree = DecisionTreeClassifier()\n\n\nnn = MLPClassifier(solver=\'lbfgs\', alpha=1e-5,\n                     hidden_layer_sizes=(1), random_state=1)\n\n\n\nif __name__ == \'__main__\':\n       # reading the csv file\n    df = pd.read_csv("data.csv")\n    X = df.iloc[:, :-1] # Features\n    y = df.iloc[:, -1] # Target variable\n\n    li_df = []\n    for i in range(0,10):\n        li_df.append(build_table(X,y,[decision_tree,"Decision Tree",False],\n                                [nn, "Artificial Neural Network",True]))\n\n    averages = pd.concat([each.stack() for each in li_df],axis=1)\\\n                .apply(lambda x:x.mean(),axis=1)\\\n                .unstack()\n    print(averages)',
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
