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
    'version': '0.1.1',
    'description': 'Text utilities library by Pinecone.io',
    'long_description': '# Pinecone text client\n\nText utilities to work with Pinecone.\n\n## Sparse encoding\n\nTo convert your own text corpus to sparse vectors, you can either use BM25 or Splade. \nFor more information, see the [Pinecone documentation](https://docs.pinecone.io/docs/hybrid-search).\n\n### BM25\n```python\nfrom pinecone_text.sparse import BM25\n\ncorpus = ["The quick brown fox jumps over the lazy dog",\n          "The lazy dog is brown",\n          "The fox is brown"]\n\n# Initialize BM25 and fit the corpus\nbm25 = BM25(tokenizer=lambda x: x.split())\nbm25.fit(corpus)\n\n# Encode a new document (for upsert to Pinecone index)\ndoc_sparse_vector = bm25.encode_document("The brown fox is quick") \n# {"indices": [102, 18, 12, ...], "values": [0.21, 0.38, 0.15, ...]}\n\n# Encode a query (for search in Pinecone index)\nquery_sparse_vector = bm25.encode_query("Which fox is brown?")\n# {"indices": [102, 16, 18, ...], "values": [0.21, 0.11, 0.15, ...]}\n\n# store BM25 params as json\nbm25.store_params("bm25_params.json")\n\n# load BM25 params from json\nbm25.load_params("bm25_params.json")\n```\n\n### Splade\n```python\nfrom pinecone_text.sparse import Splade\n\ncorpus = ["The quick brown fox jumps over the lazy dog",\n          "The lazy dog is brown",\n          "The fox is brown"]\n\n# Initialize Splade\nsplade = Splade()\n\n# encode a batch of documents/queries\nsparse_vectors = splade(corpus)\n# [{"indices": [102, 18, 12, ...], "values": [0.21, 0.38, 0.15, ...]}, ...]\n```',
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
