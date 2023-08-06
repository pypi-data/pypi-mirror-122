# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['episimlab',
 'episimlab.models',
 'episimlab.partition',
 'episimlab.setup',
 'episimlab.setup.greek',
 'episimlab.utils']

package_data = \
{'': ['*']}

install_requires = \
['dask[dataframe,distributed]>=2021.4.0,<2022.0.0',
 'graphviz>=0.16,<0.17',
 'matplotlib>=3.4.1,<4.0.0',
 'networkx>=2.6.2,<3.0.0',
 'numpy>=1.20.2,<2.0.0',
 'xarray-simlab>=0.5.0,<0.6.0',
 'xarray>=0.17.0,<0.18.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.10"': ['scipy>=1.6.2,<2.0.0']}

setup_kwargs = {
    'name': 'episimlab',
    'version': '2.0.0',
    'description': 'Framework for modular development of epidemiological models',
    'long_description': None,
    'author': 'Ethan Ho',
    'author_email': 'eho@tacc.utexas.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
