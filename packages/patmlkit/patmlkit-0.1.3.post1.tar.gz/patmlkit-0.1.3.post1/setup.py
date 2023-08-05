# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patmlkit']

package_data = \
{'': ['*']}

install_requires = \
['imagesize>=1.4.1,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pyclipper>=1.3.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'patmlkit',
    'version': '0.1.3.post1',
    'description': 'Pain and tears ML kit - library created to support my journey via PHD',
    'long_description': 'None',
    'author': 'Michal Karol',
    'author_email': 'michal.p.karol@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
