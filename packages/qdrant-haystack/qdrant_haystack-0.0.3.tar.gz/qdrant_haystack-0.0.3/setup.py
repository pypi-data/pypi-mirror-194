# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['qdrant_haystack', 'qdrant_haystack.document_stores']

package_data = \
{'': ['*']}

install_requires = \
['farm-haystack>=1.13.0,<2.0.0', 'qdrant-client>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'qdrant-haystack',
    'version': '0.0.3',
    'description': 'An integration of Qdrant ANN vector database backend with Haystack',
    'long_description': '# qdrant-haystack\n\nAn integration of [Qdrant](https://qdrant.tech) vector database with [Haystack](https://haystack.deepset.ai/)\nby [deepset](https://www.deepset.ai).\n\nThe library finally allows using Qdrant as a document store, and provides an in-place replacement\nfor any other vector embeddings store. Thus, you should expect any kind of application to be working\nsmoothly just by changing the provider to `QdrantDocumentStore`.\n\n## Installation\n\n`qdrant-haystack` might be installed as any other Python library, using pip or poetry:\n\n```bash\npip install qdrant-haystack\n```\n\n```bash\npoetry add qdrant-haystack\n```\n\n## Usage\n\nOnce installed, you can already start using `QdrantDocumentStore` as any other store that supports\nembeddings.\n\n```python\nfrom qdrant_haystack import QdrantDocumentStore\n\ndocument_store = QdrantDocumentStore(\n    host="localhost",\n    index="Document",\n    embedding_dim=512,\n    recreate_index=True,\n)\n```\n\nThe list of parameters accepted by `QdrantDocumentStore` is complementary to those used in the\nofficial [Python Qdrant client](https://github.com/qdrant/qdrant_client).\n',
    'author': 'Kacper Łukawski',
    'author_email': 'kacper.lukawski@qdrant.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<=3.11',
}


setup(**setup_kwargs)
