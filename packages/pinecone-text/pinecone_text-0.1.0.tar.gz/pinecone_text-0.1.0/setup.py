# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinecone_text', 'pinecone_text.sparse']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.2.1,<2.0.0',
 'torch>=1.13.1,<2.0.0',
 'transformers>=4.26.1,<5.0.0']

setup_kwargs = {
    'name': 'pinecone-text',
    'version': '0.1.0',
    'description': 'D',
    'long_description': '',
    'author': 'Pinecone.io',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
