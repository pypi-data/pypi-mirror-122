# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sjtop']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24.1', 'shioaji>=0.3.3.dev3', 'textual>=0.1.12,<0.2.0']

entry_points = \
{'console_scripts': ['sjtop = sjtop.__main__:main']}

setup_kwargs = {
    'name': 'sjtop',
    'version': '0.1.2',
    'description': 'Terminal User Interface for Shioaji',
    'long_description': '# sjtop (WIP)\n\nsjtop is a TUI (Terminal User Interface) for Shioaji using Textual to develop.\n\nNOTE: This project is currently a work in progress\n\n### Installation\n```\npip install sjtop\n```\n\n### Usage\n```\nsjtop\n```\n\n### Preview\n\n![screenshot](./imgs/sjtop.gif)',
    'author': 'Yvictor',
    'author_email': 'yvictor3141@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yvictor/sjtop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
