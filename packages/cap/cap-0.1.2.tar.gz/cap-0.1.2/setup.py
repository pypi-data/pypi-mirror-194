# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cap']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.22.1,<0.23.0']

setup_kwargs = {
    'name': 'cap',
    'version': '0.1.2',
    'description': 'Cap: lightweight package for use network captures',
    'long_description': '# Cap: lightweight package for use network captures\n\n[![Build Status](https://travis-ci.org/netanelrevah/cap.svg?branch=develop)](https://travis-ci.org/netanelrevah/cap) [![PyPI version](https://img.shields.io/pypi/v/cap.svg)](https://pypi.python.org/pypi/cap/) [![PyPI downloads](https://img.shields.io/pypi/dm/cap.svg)](https://pypi.python.org/pypi/cap/)\n\nThe idea is to read and write capture files like it is really a serialized data. The API is ment to be close as possible to json and pickle APIs.\n\n## Installation:\ninstall the package by:\n``` bash\npip install cap\n```\nor from the source:\n``` bash\npython setup.py install\n```\n## Usage:\n### read cap:\n```python\nimport cap\ncaptured_packets = cap.load(open("C:\\\\test.cap", "rb"))\n```\n### filter about somthing\n```python\nip_v4_captured_packet = []\nfor captured_packet in captured_packets:\n    if captured_packet.data[12:14] == \'\\x08\\x00\':\n        ip_v4_captured_packet.append(p)\n```\n### dump filtered packets\n```python\ncap.dump(ip_v4_captured_packet, open(\'C:\\\\new_test.cap\', "wb"))\n```\n\nHave a nice use and please report about problems and issues.\nThank you.\n',
    'author': 'Netanel Revah',
    'author_email': 'netanelrevah@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
