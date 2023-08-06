# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vretcity']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.0,<2.0.0', 'pandas>=1.3.3,<2.0.0', 'plotly>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'vretcity',
    'version': '0.1.1',
    'description': 'Package to preprocess and analyse data from the vretcity project at NUDZ',
    'long_description': None,
    'author': 'Lukáš Hejtmánek',
    'author_email': 'hejtmy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
