# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.templates']

package_data = \
{'': ['*'], 'understory': ['static/*']}

install_requires = \
['webint-auth>=0.0.7,<0.0.8',
 'webint-code>=0.0.13,<0.0.14',
 'webint-data>=0.0.46,<0.0.47',
 'webint-editor>=0.0.155,<0.0.156',
 'webint-guests>=0.0.4,<0.0.5',
 'webint-live>=0.0.8,<0.0.9',
 'webint-media>=0.0.51,<0.0.52',
 'webint-mentions>=0.0.9,<0.0.10',
 'webint-owner>=0.0.5,<0.0.6',
 'webint-player>=0.0.2,<0.0.3',
 'webint-posts>=0.0.8,<0.0.9',
 'webint-search>=0.0.5,<0.0.6',
 'webint-system>=0.0.3,<0.0.4',
 'webint-tracker>=0.0.3,<0.0.4']

entry_points = \
{'websites': ['understory = understory:app']}

setup_kwargs = {
    'name': 'understory',
    'version': '0.1.10',
    'description': 'a decentralized social platform',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/understory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
