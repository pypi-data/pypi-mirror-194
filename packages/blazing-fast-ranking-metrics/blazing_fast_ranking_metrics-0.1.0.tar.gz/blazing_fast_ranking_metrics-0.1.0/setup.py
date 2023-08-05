# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blazing_fast_ranking_metrics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0', 'polars>=0.16.8,<0.17.0']

setup_kwargs = {
    'name': 'blazing-fast-ranking-metrics',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mmarin',
    'author_email': 'mikhail.marin@sbermarket.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
