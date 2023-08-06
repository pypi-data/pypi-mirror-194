# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gaql_console']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'google-ads>=20.0.0,<21.0.0',
 'prompt-toolkit>=3.0.24,<4.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['gaql = gaql_console.console:main']}

setup_kwargs = {
    'name': 'gaql-console',
    'version': '0.1.4',
    'description': 'Google Ads Query Language Interactive Console',
    'long_description': 'None',
    'author': 'Piotr Kilczuk',
    'author_email': 'piotr@kilczuk.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
