# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clebs_puc_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pandas>=1.3.3,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'clebs_puc_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'clebs-puc-csv-converter',
    'version': '0.1.1',
    'description': 'Convert csv to json. Publishing only for learning purposes at PUC.',
    'long_description': None,
    'author': 'Clebson Cardoso',
    'author_email': 'clebsondm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
