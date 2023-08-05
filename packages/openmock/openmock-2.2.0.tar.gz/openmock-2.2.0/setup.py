# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openmock', 'openmock.behaviour', 'openmock.utilities']

package_data = \
{'': ['*']}

install_requires = \
['opensearch-py', 'python-dateutil', 'python-ranges==0.2.1']

setup_kwargs = {
    'name': 'openmock',
    'version': '2.2.0',
    'description': 'Python OpenSearch Mock for test purposes',
    'long_description': "# Openmock\n\nMock/fake of opensearch library, allows you to mock opensearch-py\n\nFork of Python Elasticsearch(TM) Mock. Sometimes the developers who work with elasticsearch (TM),\ndon't really have any input in choice of host and need to get work done.\n\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/openmock) [![Downloads](https://pepy.tech/badge/openmock/month)](https://pepy.tech/project/openmock/month)\n\n## Installation\n\n```shell\npip install openmock\n```\n\n## Usage\n\nTo use Openmock, decorate your test method with **@openmock** decorator:\n\n```python\nfrom unittest import TestCase\n\nfrom openmock import openmock\n\n\nclass TestClass(TestCase):\n\n    @openmock\n    def test_should_return_something_from_opensearch(self):\n        self.assertIsNotNone(some_function_that_uses_opensearch())\n```\n\n### Custom Behaviours\n\nYou can also force the behaviour of the OpenSearch instance by importing the `openmock.behaviour` module:\n\n```python\nfrom unittest import TestCase\n\nfrom openmock import behaviour\n\n\nclass TestClass(TestCase):\n\n    ...\n\n    def test_should_return_internal_server_error_when_simulate_server_error_is_true(self):\n        behaviour.server_failure.enable()\n        ...\n        behaviour.server_failure.disable()\n```\n\nYou can also disable all behaviours by calling `behaviour.disable_all()` (Consider put this in your `def tearDown(self)` method)\n\n#### Available Behaviours\n\n* `server_failure`: Will make all calls to OpenSearch returns the following error message:\n    ```python\n    {\n        'status_code': 500,\n        'error': 'Internal Server Error'\n    }\n    ```\n\n## Code example\n\nLet's say you have a prod code snippet like this one:\n\n```python\nimport opensearchpy\n\nclass FooService:\n\n    def __init__(self):\n        self.es = opensearchpy.OpenSearch(hosts=[{'host': 'localhost', 'port': 9200}])\n\n    def create(self, index, body):\n        es_object = self.es.index(index, body)\n        return es_object.get('_id')\n\n    def read(self, index, id):\n        es_object = self.es.get(index, id)\n        return es_object.get('_source')\n\n```\n\nThen you should be able to test this class by mocking OpenSearch using the following test class:\n\n```python\nfrom unittest import TestCase\nfrom openmock import openmock\nfrom foo.bar import FooService\n\nclass FooServiceTest(TestCase):\n\n    @openmock\n    def should_create_and_read_object(self):\n        # Variables used to test\n        index = 'test-index'\n        expected_document = {\n            'foo': 'bar'\n        }\n\n        # Instantiate service\n        service = FooService()\n\n        # Index document on OpenSearch\n        id = service.create(index, expected_document)\n        self.assertIsNotNone(id)\n\n        # Retrive document from OpenSearch\n        document = service.read(index, id)\n        self.assertEquals(expected_document, document)\n\n```\n\n## Notes:\n\n- The mocked **search** method returns **all available documents** indexed on the index with the requested document type.\n- The mocked **suggest** method returns the exactly suggestions dictionary passed as body serialized in OpenSearch.suggest response. **Attention:** If the term is an *int*, the suggestion will be ```python term + 1```. If not, the suggestion will be formatted as ```python {0}_suggestion.format(term) ```.\nExample:\n\t- **Suggestion Body**:\n\t```python\n    suggestion_body = {\n        'suggestion-string': {\n            'text': 'test_text',\n            'term': {\n                'field': 'string'\n            }\n        },\n        'suggestion-id': {\n            'text': 1234567,\n            'term': {\n                'field': 'id'\n            }\n        }\n    }\n    ```\n    - **Suggestion Response**:\n    ```python\n    {\n        'suggestion-string': [\n            {\n                'text': 'test_text',\n                'length': 1,\n                'options': [\n                    {\n                        'text': 'test_text_suggestion',\n                        'freq': 1,\n                        'score': 1.0\n                    }\n                ],\n                'offset': 0\n            }\n        ],\n        'suggestion-id': [\n            {\n                'text': 1234567,\n                'length': 1,\n                'options': [\n                    {\n                        'text': 1234568,\n                        'freq': 1,\n                        'score': 1.0\n                    }\n                ],\n                'offset': 0\n            }\n        ],\n    }\n    ```\n\n## Testing\n\nPreferred for testing one version of python.\n```bash\npytest test\n```\n\nWon't catch pytest tests.\n```bash\npython -m unittest\n```\n\nWe are trying to support a full matrix of openmock versions and python versions 3.6+. This is slow.\n```bash\ntox\n```\n\n## Changelog\n\n#### 2.1.0:\n- Update function (Thanks!)\n- tox runs against full matrix\n- Range queries (Thanks!)\n\n#### 2.0.0:\n- Fork from elasticmock\n\n## License\nMIT with normalize_host.py being Apache 2 from Elasticsearch.\n",
    'author': 'Marcos Cardoso',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/matthewdeanmartin/openmock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
