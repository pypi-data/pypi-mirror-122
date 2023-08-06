# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goa']

package_data = \
{'': ['*']}

install_requires = \
['imageio-ffmpeg>=0.4.5,<0.5.0',
 'imageio>=2.9.0,<3.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'goa',
    'version': '0.1.0',
    'description': 'goa (Global Optimization Animations) helps visualize the execution of some global optimization algorithms on a given problem.',
    'long_description': None,
    'author': 'Lorenzo Palloni',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
