# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigwood',
 'bigwood.bin',
 'bigwood.data',
 'bigwood.data.plotting',
 'bigwood.test']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0', 'numpy>=1.22.4,<2.0.0', 'pandas>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['getmyip = bigwood.bin.getip:main']}

setup_kwargs = {
    'name': 'bigwood',
    'version': '0.0.9',
    'description': 'A basic package for some of the utils I use.',
    'long_description': 'None',
    'author': 'Chris Woodall',
    'author_email': 'christopherhwoodall@gmail.com',
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
