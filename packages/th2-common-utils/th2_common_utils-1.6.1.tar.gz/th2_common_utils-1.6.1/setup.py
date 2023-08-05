# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['th2_common_utils', 'th2_common_utils.converters']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.1,<4.0.0',
 'sortedcollections>=2.0.0,<3.0.0',
 'th2-grpc-common>=3.11,<4.0']

setup_kwargs = {
    'name': 'th2-common-utils',
    'version': '1.6.1',
    'description': 'Python library with useful functions for developers and QA needs',
    'long_description': '# th2-common-utils-py (1.6.1)\nPython library with useful functions for **developers and QA needs**. Check the [Wiki](https://github.com/th2-net/th2-common-utils-py/wiki) for instructions and examples.\n\n## Installation\n```\npip install th2-common-utils\n```\n',
    'author': 'TH2-devs',
    'author_email': 'th2-devs@exactprosystems.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/th2-net/th2-common-utils-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
