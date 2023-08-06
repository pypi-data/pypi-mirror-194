# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pubnet', 'pubnet.data', 'pubnet.network', 'pubnet.network._edge']

package_data = \
{'': ['*'], 'pubnet': ['_src/*']}

install_requires = \
['igraph>=0.10,<0.11',
 'matplotlib>=3.5,<4.0',
 'numpy>=1.23,<2.0',
 'pandas>=1.4,<2.0',
 'pyarrow>=9.0,<10.0',
 'scipy>=1.9,<2.0']

setup_kwargs = {
    'name': 'pubnet',
    'version': '0.6.1',
    'description': 'A python package for storing and working with publication data in graph form.',
    'long_description': '** PubNet publication networks\nProvides data types for managing publication networks as a set of graphs.\n\n~PubNet~ provides functions for downloading, storing, manipulating, and saving publication networks.\nNetworks can come from common online sources like pubmed and crossref.\n\n** Installation\n#+begin_src bash :eval no\npip install --user pubnet\n#+end_src\n\n** More help\nSee [[https://net-synergy.gitlab.io/pubnet][Documentation]]\n',
    'author': 'David Connell',
    'author_email': 'davidconnell12@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/net-synergy/pubnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
