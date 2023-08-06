# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valoff_ie_api', 'valoff_ie_api.tests']

package_data = \
{'': ['*']}

install_requires = \
['icontract>=2.5.0,<3.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'valoff-ie-api',
    'version': '0.1.0',
    'description': 'An unofficial Python API for the Valuation Office REST API',
    'long_description': None,
    'author': 'Rowan Molony',
    'author_email': 'rowan.molony@codema.ie',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
