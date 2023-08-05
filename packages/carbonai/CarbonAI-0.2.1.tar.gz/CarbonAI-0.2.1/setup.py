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
    'version': '0.2.1',
    'description': 'Monitor the power consumption of a function',
    'long_description': '# CarbonAI\n\nThis project aims at creating a python package that allows you to monitor the power consumption of any python function.\n\n## Documentation\n\nThe complete documentation is available [here](https://capgemini-invent-france.github.io/CarbonAI/).\n\n## Getting started\n### Install\n\nFirst of all you need to install the intel utility allowing you to monitor power consumption ([support](https://software.intel.com/en-us/articles/intel-power-gadget)):\n* [Windows](https://software.intel.com/file/823776/download)\n* [MacOS](https://software.intel.com/sites/default/files/managed/91/6b/Intel%20Power%20Gadget.dmg)\n* Linux, no need to install any software\n\nTo install this package :\n```sh\npip install carbonai\n```\n\n### Example\n\nThere are several ways to use this package depending on how you develop.\nYou just have to import the `PowerMeter` object, initialize it and call the function you want to monitor.\nPlease insert a description of the running function, the dataset, the model, any info would be useful.\n\n#### Function decorator\nTo monitor the power consumption of a function, follow this example:\n```python\nfrom carbonai import PowerMeter\npower_meter = PowerMeter(project_name="MNIST classifier")\n\n@power_meter.measure_power(\n  package="sklearn",\n  algorithm="RandomForestClassifier",\n  data_type="tabular",\n  data_shape=<your_data>.shape,\n  algorithm_params="n_estimators=300, max_depth=15",\n  comments="Classifier trained on the MNIST dataset, 3rd test"\n)\ndef my_func(arg1, arg2, ...):\n  # Do something\n```\n\n#### Using the with statement\nTo monitor the power consumption of some specific inline code, you can use with statements\n\n```python\nfrom carbonai import PowerMeter\npower_meter = PowerMeter(project_name="MNIST classifier")\n\nwith power_meter(\n  package="sklearn",\n  algorithm="RandomForestClassifier",\n  data_type="tabular",\n  data_shape=<your_data>.shape,\n  algorithm_params="n_estimators=300, max_depth=15",\n  comments="Classifier trained on the MNIST dataset, 3rd test"\n):\n  # Do something\n```\n\n## Contribute\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n\nYou can find details on how to contribute in [our guide](CONTRIBUTING.md)\n',
    'author': 'Capgemini Invent - Martin Chauvin, Francois Lemeille, Jordan Toh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Capgemini-Invent-France/CarbonAI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
