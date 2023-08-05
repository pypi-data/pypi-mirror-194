# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melid', 'melid.base', 'melid.router']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5-Qt5==5.15.2', 'PyQt5-sip==12.11.1', 'PyQt5==5.15.9']

setup_kwargs = {
    'name': 'melid',
    'version': '1.0.4',
    'description': 'Melid',
    'long_description': '# Melid\n\nMelid is a PyQt5 Library for Desktop Applications containing commonly used utils and advanced widget implementations in very simple forms.\n\n# Features\n\n- [x] router\n- [ ] store (state management)\n- [ ] hot-reload -> in progress\n- [x] CSS Processor (TailwindCSS Syntax)\n\n# Install\n\n```sh\n$ pip install melid\n```\n\n# Usage\n\nCheck the examples folder for usage examples.\n\n```sh\n$ git clone https://github.com/dev-47/melid.git\n$ cd examples/basic\n$ python main.py\n```\n',
    'author': 'Mohammed Al Ameen',
    'author_email': 'ameenmohammed2311@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
