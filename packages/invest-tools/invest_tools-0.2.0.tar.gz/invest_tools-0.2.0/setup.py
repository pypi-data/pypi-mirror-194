# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invest_tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'statsmodels>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'invest-tools',
    'version': '0.2.0',
    'description': 'Tools to manage portfolio risk analysis',
    'long_description': '# invest-tools\n\n[![PyPI version](https://badge.fury.io/py/invest-tools.svg)](https://badge.fury.io/py/invest-tools)\n[![codecov](https://codecov.io/gh/leo-jp-edwards/invest-tools/branch/main/graph/badge.svg?token=C1W8MZFS80)](https://codecov.io/gh/leo-jp-edwards/invest-tools)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nTools to manage portfolio risk analysis\n',
    'author': 'leo',
    'author_email': 'leojpedwards@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
