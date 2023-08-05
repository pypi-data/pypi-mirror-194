# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invest_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'invest-tools',
    'version': '0.1.0',
    'description': 'Tools to manage portfolio risk analysis',
    'long_description': '# invest-tools\n\n[![codecov](https://codecov.io/gh/leo-jp-edwards/invest-tools/branch/main/graph/badge.svg?token=C1W8MZFS80)](https://codecov.io/gh/leo-jp-edwards/invest-tools)\n\nTools to manage portfolio risk analysis\n',
    'author': 'leo',
    'author_email': 'leojpedwards@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
