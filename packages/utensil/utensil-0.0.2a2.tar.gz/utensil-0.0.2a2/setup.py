# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utensil',
 'utensil.constant',
 'utensil.general',
 'utensil.loopflow',
 'utensil.loopflow.functions',
 'utensil.random_search']

package_data = \
{'': ['*']}

extras_require = \
{'loguru': ['loguru>=0.5.3,<0.6.0'],
 'loopflow': ['PyYAML>=5.4.1,<6.0.0',
              'pandas>=1.3.3,<2.0.0',
              'xgboost>=1.4.2,<2.0.0',
              'scikit-learn>=1.0,<2.0']}

setup_kwargs = {
    'name': 'utensil',
    'version': '0.0.2a2',
    'description': 'A useful utensil kit for machine learning.',
    'long_description': '# Utensil\n\nUtensil is a python programming tool kit for day-to-day \nmachine learning, data mining, and information analysis, etc.\n\n## Installation\n\n``pip install utensil``\n\n## Main Functions\n\n### Machine Learning\n* parameter searching: ``utensil.random_search``\n* directed cyclic/asyclic graph work flow: ``utensil.loopflow``\n\n### Utilities\n* config setting (todo)\n* process bar (todo)\n',
    'author': 'Chou Hung-Yi',
    'author_email': 'hychou.svm@gmail.com',
    'maintainer': 'Chou Hung-Yi',
    'maintainer_email': 'hychou.svm@gmail.com',
    'url': 'https://github.com/HYChou0515/utensil',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.4,<4',
}


setup(**setup_kwargs)
