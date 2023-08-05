# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonai']

package_data = \
{'': ['*'], 'carbonai': ['data/*']}

install_requires = \
['fuzzywuzzy>=0.17.0',
 'ipython>=7.12',
 'numpy>=1.20.3',
 'pandas>=1.0.5',
 'psutil',
 'requests>=2.20.1']

setup_kwargs = {
    'name': 'carbonai',
    'version': '0.2',
    'description': 'Monitor the power consumption of a function',
    'long_description': None,
    'author': 'Capgemini Invent - Martin Chauvin, Francois Lemeille, Jordan Toh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
