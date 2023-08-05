# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_lakehouse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dora-lakehouse',
    'version': '0.0.13',
    'description': 'Dora Lakehouse',
    'long_description': "# Dora Lakehouse\n\n[![Python testing](https://github.com/doraproject/lakehouse/actions/workflows/python-testing.yml/badge.svg)](https://github.com/doraproject/lakehouse/actions/workflows/python-testing.yml)\n[![PyPI](https://img.shields.io/pypi/v/dora-lakehouse)](https://pypi.org/project/dora-lakehouse/) \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dora-lakehouse)\n\nDora's lakehouse software development kit\n\n## Getting Started\n\nYou can install the library using pip:\n\n```sh\npip install dora-lakehouse\n```\n\n## Getting Help\n\nWe use **GitHub** [issues](https://github.com/doraproject/lakehouse/issues) for tracking [bugs](https://github.com/doraproject/lakehouse/labels/bug), [questions](https://github.com/doraproject/lakehouse/labels/question) and [feature requests](https://github.com/doraproject/lakehouse/labels/enhancement).\n\n## Contributing\n\nWe value feedback and contributions from our community. Please read through this [CONTRIBUTING](.github/CONTRIBUTING.md) document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your contribution.\n\n---\n\n[Dora Project](https://github.com/doraproject) is a recent open-source project based on technology developed at [Compasso UOL](https://compassouol.com/)\n",
    'author': 'Didone',
    'author_email': 'didone@live.com',
    'maintainer': 'DataLabs',
    'maintainer_email': 'time.dataanalytics.datalabs@compasso.com.br',
    'url': 'https://github.com/doraproject/lakehouse',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
