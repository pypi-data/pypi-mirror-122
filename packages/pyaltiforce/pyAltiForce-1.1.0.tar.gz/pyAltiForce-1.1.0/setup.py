# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaltiforce']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4,<4.0', 'numpy>=1.21,<2.0']

entry_points = \
{'console_scripts': ['altiforce = pyaltiforce.altiforce:cli']}

setup_kwargs = {
    'name': 'pyaltiforce',
    'version': '1.1.0',
    'description': 'Python Parsing for AltiForce GoPro Backpack CSVs.',
    'long_description': "# pyAltiForce\nPython Parsing for AltiForce GoPro Backpack CSVs\n\nThe CSV file is processed and a plot of time vs. total acceleration is displayed.\n\n## Usage\nCalling `pyAltiForce` from the command line with no arguments opens a file selection GUI for the user to select a single CSV file to process and display.\n\nCalling `pyAltiForce` with the optional `-f` or `--file` flag will allow the user to specify a single CSV file to process.\n\nExamples Include:\n\n    python pyAltiForce -f './Data/GOPR0024.CSV'\n    python pyAltiForce --file 'C:/My Data/GOPR0024.CSV'\n",
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
