# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elkplot', 'elkplot.text']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'hypothesis>=6.67.1,<7.0.0',
 'pint>=0.20.1,<0.21.0',
 'pyglet==1.5.27',
 'pyserial>=3.5,<4.0',
 'pytest>=7.2.1,<8.0.0',
 'rtree>=1.0.1,<2.0.0',
 'shapely>=2.0.1,<3.0.0',
 'svg-path>=6.2,<7.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['elk = elkplot.cli:cli']}

setup_kwargs = {
    'name': 'elkplot',
    'version': '0.1.1',
    'description': 'A library for making and executing generative art for the Axidraw line of pen plotters.',
    'long_description': '# ElK Plot\n\nA library for making and executing generative art for the Axidraw line of pen plotters.',
    'author': 'El Kaplan',
    'author_email': 'kaplan.el.j@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
