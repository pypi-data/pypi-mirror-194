# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nicolasbancel_de_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['deng = nicolasbancel_de_toolkit.main:cli']}

setup_kwargs = {
    'name': 'nicolasbancel-de-toolkit',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Nicolas Bancel',
    'author_email': 'nicolas.bancel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
