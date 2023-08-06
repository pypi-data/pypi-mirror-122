# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verdandi']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['verdandi = verdandi.main:main']}

setup_kwargs = {
    'name': 'verdandi',
    'version': '0.1.3',
    'description': 'Benchmarking framework',
    'long_description': '# verdandi\nBenchmarking framework \n',
    'author': 'Kamil Marut',
    'author_email': 'kamil@kamilmarut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exler/verdandi',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
