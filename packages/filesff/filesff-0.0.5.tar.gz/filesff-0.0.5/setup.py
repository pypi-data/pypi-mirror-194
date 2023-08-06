# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filesff', 'filesff.core']

package_data = \
{'': ['*']}

extras_require = \
{'cap': ['cap>=0.1.3,<0.2.0'],
 'msgpack': ['msgpack>=1.0.4,<2.0.0'],
 'protobuf': ['protobuf>=4.22.0,<5.0.0'],
 'ujson': ['ujson>=5.6.0,<6.0.0']}

setup_kwargs = {
    'name': 'filesff',
    'version': '0.0.5',
    'description': 'Files for Fun; Python Utilities',
    'long_description': '# FilesFF - Files For Fun\n\n[![PyPI version](https://img.shields.io/pypi/v/filesff.svg)](https://pypi.python.org/pypi/filesff/) [![PyPI downloads](https://img.shields.io/pypi/dm/filesff.svg)](https://pypi.python.org/pypi/filesff/)\n\n* python package to work with file handles\n* use handles of files as parameters without keeping open files\n* replace file handles easily with mocks\n* handle many file types with generic protocol\n\nto install\n\n```shell\npip install filesff\n```\n\n## Usage\n\nread a json from gzip compressed file:\n\n```python\naccessor = json_file_accessor("./file.gz", GzippedFileHandle)\naccessor.dump({"json": "data"})\n```\n\nwrite a protobuf into a temp file\n```shell\npip install fileff[protobuf]\n```\n\n```python\nfrom google.protobuf.timestamp_pb2 import Timestamp\n\naccessor = temp_protobuf_file_accessor()\nnow = Timestamp()\nnow.FromDatetime(datetime.now())\naccessor.dump(now)\n\nloaded_now = accessor.load(message_cls=Timestamp)\n```\n\nimplement new file format:\n\n```python\nclass NewFileFormatter(FullTextFileFormatter):\n    def load(self, reader: TextIO, **_) -> AnyStr:\n        return reader.read().replace("a", "e")\n\n    def dump(self, writer: TextIO, value: Any, **_):\n        writer.write(value.replace("e", "a"))\n```\n\nuse it \n```python\nfile_accessor = FullFileAccessor.of("./path.ae", NewFileFormatter())\nfile_accessor.dump("ababab")\n```\n\n\n',
    'author': 'Netanel Revah',
    'author_email': 'netanelrevah@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
