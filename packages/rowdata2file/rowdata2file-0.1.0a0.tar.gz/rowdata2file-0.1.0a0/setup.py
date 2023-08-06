# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rowdata2file']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'rich>=13.3.1,<14.0.0',
 'set-loglevel>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['rowdata2file = rowdata2file.__main__:app']}

setup_kwargs = {
    'name': 'rowdata2file',
    'version': '0.1.0a0',
    'description': 'Convert rowdata (ag-grid) to a file for python-shell use',
    'long_description': '# rowdata2file\n[![pytest](https://github.com/ffreemt/rowdata2file/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/rowdata2file/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/rowdata2file.svg)](https://badge.fury.io/py/rowdata2file)\n\nConvert rowdata (ag-grid) to a file for python-shell use\n\n## Install it\n\n```shell\npip install rowdata2file\n# pip install git+https://github.com/ffreemt/rowdata2file\n# poetry add git+https://github.com/ffreemt/rowdata2file\n# git clone https://github.com/ffreemt/rowdata2file && cd rowdata2file\n```\n\n## Use it\n```python\nfrom rowdata2file import rowdata2file\n\n```\n',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/rowdata2file',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
