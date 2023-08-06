# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arti',
 'arti.annotations',
 'arti.artifacts',
 'arti.backends',
 'arti.executors',
 'arti.fingerprints',
 'arti.formats',
 'arti.graphs',
 'arti.internal',
 'arti.io',
 'arti.partitions',
 'arti.producers',
 'arti.statistics',
 'arti.storage',
 'arti.thresholds',
 'arti.types',
 'arti.versions',
 'arti.views']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0',
 'frozendict>=2.0.6,<3.0.0',
 'multimethod>=1.6,<2.0',
 'parse>=1.19.0,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pyfarmhash>=0.2.2,<0.3.0',
 'python-box>=5.4.1,<6.0.0',
 'setuptools>=58.2.0,<59.0.0',
 'sgqlc>=14.1,<15.0',
 'toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'arti',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'Replica',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
