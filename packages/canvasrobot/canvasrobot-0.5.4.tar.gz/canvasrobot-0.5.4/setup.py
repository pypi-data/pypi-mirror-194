# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canvasrobot', 'canvasrobot.entities']

package_data = \
{'': ['*']}

install_requires = \
['canvasapi>=3.0.0,<3.1.0',
 'keyring',
 'openpyxl>=3.0.10,<4.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'pydal',
 'requests>=2.28.1,<2.29.0',
 'rich',
 'toml']

setup_kwargs = {
    'name': 'canvasrobot',
    'version': '0.5.4',
    'description': 'Library which uses Canvasapi https://canvasapi.readthedocs.io/en/stable/getting-started.html to provide a CanvasRobot class.',
    'long_description': '# CanvasRobot\nLibrary which uses\n[Canvasapi](https://canvasapi.readthedocs.io/en/stable/getting-started.html)\nto provide a CanvasRobot class.\nUsed in word2quiz library.\n\n[![PyPI version](https://badge.fury.io/py/canvasrobot.svg)]',
    'author': 'Nico de Groot',
    'author_email': 'ndegroot0@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0.0',
}


setup(**setup_kwargs)
