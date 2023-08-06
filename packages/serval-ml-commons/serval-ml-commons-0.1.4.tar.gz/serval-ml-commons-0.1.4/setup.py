# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlc',
 'mlc.classifier',
 'mlc.constraints',
 'mlc.datasets',
 'mlc.datasets.samples',
 'mlc.metrics',
 'mlc.models',
 'mlc.models.samples',
 'mlc.preprocessing',
 'mlc.transformers']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.0.0',
 'numpy>=1.21.0',
 'pandas>=1.1.5',
 'requests>=2.27',
 'scikit-learn>=0.24.0',
 'uuid>=1.30,<2.0']

extras_require = \
{'torch': ['torch>=1.12.1,<1.13.0']}

setup_kwargs = {
    'name': 'serval-ml-commons',
    'version': '0.1.4',
    'description': 'SerVal Machine learning commons is a tools box that ease the development of ML experiments at SerVal.',
    'long_description': 'None',
    'author': 'Thibault Simonetto',
    'author_email': 'thibault.simonetto.001@student.uni.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
