# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt_osmosis', 'dbt_osmosis.exceptions', 'dbt_osmosis.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'dbt>=0.20.2,<0.21.0',
 'rich>=10.11.0,<11.0.0',
 'ruamel.yaml>=0.17.16,<0.18.0']

entry_points = \
{'console_scripts': ['dbt-osmosis = dbt_osmosis.main:cli']}

setup_kwargs = {
    'name': 'dbt-osmosis',
    'version': '0.2.0',
    'description': 'This package serves to cascadingly populate column level documentation as well as build model files.',
    'long_description': None,
    'author': 'Falador_wiz1',
    'author_email': 'alex@source.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
