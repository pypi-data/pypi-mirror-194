# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nohedidnt_py', 'nohedidnt_py.common']

package_data = \
{'': ['*']}

install_requires = \
['babel>=2.11.0,<3.0.0',
 'catalogue>=2.0.8,<3.0.0',
 'chardet>=5.1.0,<6.0.0',
 'charset-normalizer>=3.0.1,<4.0.0',
 'codetiming>=1.4.0,<2.0.0',
 'colour>=0.1.5,<0.2.0',
 'decorator>=5.1.1,<6.0.0',
 'deepdiff6>=6.2.0,<7.0.0',
 'devtools[pygments]>=0.10.0,<0.11.0',
 'inflect>=6.0.2,<7.0.0',
 'pycountry-convert>=0.7.2,<0.8.0',
 'pycountry>=22.3.5,<23.0.0',
 'pydantic[email]>=1.10.4,<2.0.0',
 'python-box[all]>=7.0.0,<8.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'pytz>=2022.7.1,<2023.0.0',
 'pyyaml>=6.0,<7.0',
 'suntime>=1.2.5,<2.0.0',
 'typing-extensions>=4.5.0,<5.0.0',
 'tzlocal>=4.2,<5.0',
 'urllib3>=1.26.14,<2.0.0',
 'watchdog>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'nohedidnt-py',
    'version': '0.1.1',
    'description': '',
    'long_description': "# nohedidnt_py - NoHeDidn't Python-Library\n\n[![PyPI](https://img.shields.io/pypi/v/nohedidnt_py)](https://pypi.org/project/nohedidnt-py/)\n[![codecov](https://codecov.io/gh/NoHeDidnt/nohedidnt_py/branch/main/graph/badge.svg?token=U0OQI580BA)](https://codecov.io/gh/NoHeDidnt/nohedidnt_py)\n[![Documentation Status](https://readthedocs.org/projects/nohedidnt-py/badge/?version=latest)](https://nohedidnt-py.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nohedidnt_py)](https://pypi.org/project/nohedidnt-py/)\n[![GitHub](https://img.shields.io/github/license/NoHeDidnt/nohedidnt_py)](./LICENSE)\n\nThis repo mainly serves two purposes: As an example for trying out some things on GitHub & as my collection of code I \nthink I can use again in other projects.\n\n## Links\n\n### [Documentation](https://nohedidnt-py.readthedocs.io/en/latest/)\n",
    'author': 'NoHeDidnt',
    'author_email': 'dj@nohedidnt.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
