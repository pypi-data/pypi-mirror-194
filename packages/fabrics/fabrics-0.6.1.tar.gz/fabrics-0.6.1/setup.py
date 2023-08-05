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
    'version': '0.6.1',
    'description': 'Optimization fabrics in python.',
    'long_description': '# (Geometric) Fabrics\n\n[![Build and Agents](https://github.com/maxspahn/fabrics/actions/workflows/diffGeo_agents.yml/badge.svg)](https://github.com/maxspahn/fabrics/actions/workflows/diffGeo_agents.yml)\n[![Build and Unittest](https://github.com/maxspahn/fabrics/actions/workflows/unitTest.yml/badge.svg)](https://github.com/maxspahn/fabrics/actions/workflows/unitTest.yml)\n\n**Note on development**\n> This project is still under heavy development and there is a lack of\n> documentation. I, @maxspahn, am commited to improve and maintain that package.\n> However, I rely on people like you to point me to issues and unclear sections of\n> the code. So feel free to leave issues whenever something bugs you.\n\n**fabrics ros-wrapper**\n> The fabrics-ros wrapper will released very shortly when compability is\n> verified.\n\n\nGeometric Fabrics represent a geometric approach to motion generation for\nvarious robot structures. The idea is next development step after Riemannian\nmotion policies and offer a more stable \n\n<table>\n  <tr>\n    <td><b>Holonomic robots</b></th>\n    <td><b>Non-Holonomic robots</b></th>\n  </tr> \n  <tr>\n    <td> <img src="./assets/panda_ring.gif"  alt="1" width = 360px ></td>\n    <td> <img src="./assets/panda_dynamic_avoidance.gif"  alt="1" width = 360px ></td>\n  </tr> \n  <tr>\n    <td> <img src="./assets/boxer.gif"  alt="1" width = 360px ></td>\n    <td> <img src="./assets/albert.gif"  alt="1" width = 360px ></td>\n  </tr>\n</table>\n\n\n## Installation\n\nInstall the package through pip, using \n```bash\npip3 install ".<options>"\n```\nor from pypi using\n```bash\npip3 install fabrics\n```\nOptions are [agents] and [tutorial]. Those con be installed using\n\nInstall the package through poetry, using\n```bash\npoetry install --with <option>\n```\n\n## Publications\n\nThis repository was used in several publications. The major one being\n[Dynamic Optimization Fabrics for Motion Generation](https://arxiv.org/abs/2205.08454) \nIf you are using this software, please cite:\n```bash\n@misc{https://doi.org/10.48550/arxiv.2205.08454,\n  doi = {10.48550/ARXIV.2205.08454},\n  url = {https://arxiv.org/abs/2205.08454},\n  author = {Spahn, Max and Wisse, Martijn and Alonso-Mora, Javier},\n  keywords = {Robotics (cs.RO), FOS: Computer and information sciences, FOS: Computer and information sciences},\n  title = {Dynamic Optimization Fabrics for Motion Generation},\n  publisher = {arXiv},\n  year = {2022},\n  copyright = {Creative Commons Attribution Share Alike 4.0 International}\n}\n```\nOther publications where this repository was used:\n\nhttps://github.com/maxspahn/optuna_fabrics\n```bash\n@article{https://doi.org/10.48550/arxiv.2302.06922,\n  doi = {10.48550/ARXIV.2302.06922},\n  url = {https://arxiv.org/abs/2302.06922},\n  author = {Spahn, Max and Alonso-Mora, Javier},\n  keywords = {Robotics (cs.RO), FOS: Computer and information sciences, FOS: Computer and information sciences},\n  title = {Autotuning Symbolic Optimization Fabrics for Trajectory Generation},\n  publisher = {arXiv},\n  year = {2023},\n  copyright = {Creative Commons Attribution Share Alike 4.0 International}\n}\n```\n\nhttps://github.com/tud-amr/localPlannerBench\n```bash\n@misc{https://doi.org/10.48550/arxiv.2210.06033,\n  doi = {10.48550/ARXIV.2210.06033},\n  url = {https://arxiv.org/abs/2210.06033},\n  author = {Spahn, Max and Salmi, Chadi and Alonso-Mora, Javier},\n  keywords = {Robotics (cs.RO), FOS: Computer and information sciences, FOS: Computer and information sciences},\n  title = {Local Planner Bench: Benchmarking for Local Motion Planning},\n  publisher = {arXiv},\n  year = {2022},\n  copyright = {Creative Commons Attribution Share Alike 4.0 International}\n}\n```\n\n\n## Tutorials\n\nThis repository contains brief examples corresponding to the theory presented\nin "Optimization Fabrics" by Ratliff et al. https://arxiv.org/abs/2008.02399 .\nThese examples are named according to the naming in that publication. Each\nscript is self-contained and required software is installed using \n```bash\npip install ".[tutorial]"\n```\n## Related works and websites\n\nThe work is based on some works by the NVIDIA Research Labs. Below you find a\nlist of all relevant links:\n\n# websites\nhttps://sites.google.com/nvidia.com/geometric-fabrics\n\n# paper\n- https://arxiv.org/abs/2010.14750\n- https://arxiv.org/abs/2008.02399\n- https://arxiv.org/abs/2010.14745\n- https://arxiv.org/abs/2010.15676\n- https://arxiv.org/abs/1801.02854\n\n# videos and talks\n- https://www.youtube.com/watch?v=aM9Ha2IawEo\n- https://www.youtube.com/watch?v=awiF6JjDEbo\n- https://www.youtube.com/watch?v=VsM-kdk74d8\n\n',
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tud-amr/fabrics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
