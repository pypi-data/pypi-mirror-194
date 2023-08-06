# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyapes',
 'pyapes.class_rooms',
 'pyapes.core',
 'pyapes.core.geometry',
 'pyapes.core.mesh',
 'pyapes.core.solver',
 'pyapes.core.variables',
 'pyapes.testing',
 'pyapes.tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyevtk>=1.5.0,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'tensorboard>=2.10.1,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'pyapes',
    'version': '0.0.1',
    'description': 'Python Awesome Partial differential Equation Solver',
    'long_description': 'None',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kchung@student.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
