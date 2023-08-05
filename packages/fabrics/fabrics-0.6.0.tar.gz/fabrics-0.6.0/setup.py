# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fabrics',
 'fabrics.components.energies',
 'fabrics.components.leaves',
 'fabrics.components.maps',
 'fabrics.defaults',
 'fabrics.diffGeometry',
 'fabrics.helpers',
 'fabrics.planner']

package_data = \
{'': ['*']}

install_requires = \
['casadi>=3.5.4,<4.0.0,!=3.5.5.post1,!=3.5.5.post1',
 'forwardkinematics>=1.0,<2.0',
 'geomdl>=5.3.1,<6.0.0',
 'mpscenes>=0.3,<0.4',
 'numpy>=1.15.3,<2.0.0',
 'pickle-mixin>=1.0.2,<2.0.0',
 'pyquaternion>=0.9.9,<0.10.0',
 'quaternionic>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'fabrics',
    'version': '0.6.0',
    'description': 'Optimization fabrics in python.',
    'long_description': 'None',
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
