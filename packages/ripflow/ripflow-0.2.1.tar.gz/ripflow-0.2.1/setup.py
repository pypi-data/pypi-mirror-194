# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ripflow',
 'ripflow.analyzers',
 'ripflow.connectors',
 'ripflow.connectors.sink',
 'ripflow.connectors.source',
 'ripflow.serializers']

package_data = \
{'': ['*']}

install_requires = \
['avro>=1.11.1,<2.0.0', 'numpy>=1.24.2,<2.0.0', 'pyzmq>=25.0.0,<26.0.0']

setup_kwargs = {
    'name': 'ripflow',
    'version': '0.2.1',
    'description': 'Python package to insert analysis pipelines into data streams',
    'long_description': '\n\n# <img src="docs/assets/ripflow_logo_k.svg" width="60"> ripflow Python middle layer analysis framework\n\n## Introduction\n\nripflow provides a framework to parallelize data analysis tasks in arbitrary data streams.\n\nThe package contains the Python classes to build a middle layer application that reads data from various sources and applies arbitrary analysis pipelines onto the data using overlapping worker processes. The processed data is then published via programmable sink connectors.\n\nFor more information, see the [documentation](https://soerenjalas.github.io/ripflow/).\n',
    'author': 'Soeren Jalas',
    'author_email': 'soeren.jalas@desy.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/soerenjalas/ripflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
