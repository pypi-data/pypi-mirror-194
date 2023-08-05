# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jhalog', 'jhalog._backends', 'jhalog.exception_handlers']

package_data = \
{'': ['*']}

install_requires = \
['psutil', 'webuuid']

extras_require = \
{'cloudwatch-logs': ['aioboto3', 'aiohttp>3.8']}

setup_kwargs = {
    'name': 'jhalog',
    'version': '0.1.7',
    'description': 'Jhalog (JSON HTTP Access Log) Library',
    'long_description': '![Tests](https://github.com/JGoutin/jhalog-python/workflows/tests/badge.svg)\n[![codecov](https://codecov.io/gh/JGoutin/jhalog-python/branch/main/graph/badge.svg?token=ZZrRtqsGp8)](https://codecov.io/gh/JGoutin/jhalog-python)\n[![PyPI](https://img.shields.io/pypi/v/jhalog.svg)](https://pypi.org/project/jhalog)\n\n# Jhalog (JSON HTTP Access Log) - Python library\n\nJhalog library for Python.\n\n[Jhalog Specification](https://github.com/JGoutin/jhalog-spec)\n\nWIP\n',
    'author': 'JGoutin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JGoutin/jhalog-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
