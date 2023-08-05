# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_lineage']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20.1,<0.21.0', 'omegaconf>=2.3.0,<3.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dbt-lineage = dbt_lineage.cli:app']}

setup_kwargs = {
    'name': 'dbt-lineage',
    'version': '0.0.3',
    'description': '',
    'long_description': 'None',
    'author': 'Felipe Aguirre Martinez',
    'author_email': 'felipea@kometsales.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
