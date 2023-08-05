# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaioretry']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=5.1.1', 'typing_extensions>=4.5.0']

setup_kwargs = {
    'name': 'kaioretry',
    'version': '0.9.0',
    'description': 'All in one retry and aioretry decorators',
    'long_description': '# KaioRetry\n\n[![PyPI version](https://img.shields.io/pypi/v/kaioretry?logo=pypi&style=plastic)](https://pypi.python.org/pypi/kaioretry/)\n[![Supported Python Version](https://img.shields.io/pypi/pyversions/kaioretry?logo=python&style=plastic)](https://pypi.python.org/pypi/kaioretry/)\n[![License](https://img.shields.io/pypi/l/kaioretry?color=green&logo=GNU&style=plastic)](https://github.com/Anvil/kaioretry/blob/main/LICENSE)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/kaioretry?color=magenta&style=plastic)](https://pypistats.org/packages/kaioretry)\n\n[![Pylint Static Quality Github Action](https://github.com/Anvil/kaioretry/actions/workflows/pylint.yml/badge.svg)](https://github.com/Anvil/kaioretry/actions/workflows/pylint.yml)\n[![Pylint Static Quality Github Action](https://github.com/Anvil/kaioretry/actions/workflows/python-app.yml/badge.svg)](https://github.com/Anvil/kaioretry/actions/workflows/python-app.yml)\n\n\nKaioRetry is (yet another) retry decorator implementation, which is\nclearly inspired by the original\n[retry](https://pypi.org/project/retry) module and is actually\nbackward compatible with it.\n\n# Basic usage\n\nTransparently perform retries on failures:\n\n```python\n\nfrom kaioretry import retry, aioretry\n\n\n@retry(exceptions=ValueError, tries=2)\ndef some_func(...):\n    ...\n\n\n@aioretry(exceptions=(ValueError, SomeOtherError), tries=-1, delay=1)\nasync def some_coroutine(...):\n    ...\n\n```\n\n# Documentation\n\nIf you care to read more, a more lengthy documentation is available on\n[readthedocs](https://kaioretry.readthedocs.io/en/latest/).\n\n\n### Feedback welcome.\n',
    'author': 'Damien Nadé',
    'author_email': 'anvil.github+kaioretry@livna.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Anvil/kaioretry/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
