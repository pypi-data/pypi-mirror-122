# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_pull_request']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'attrs>=21.2.0,<22.0.0',
 'click>=8.0.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'poetry-dynamic-versioning==0.13.1']

entry_points = \
{'console_scripts': ['apr = auto_pull_request.parser:main']}

setup_kwargs = {
    'name': 'auto-pull-request',
    'version': '7.1.4',
    'description': '',
    'long_description': None,
    'author': 'ruth-seven',
    'author_email': '1098057570@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
