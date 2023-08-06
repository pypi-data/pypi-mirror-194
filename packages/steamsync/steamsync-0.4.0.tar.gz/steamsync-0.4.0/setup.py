# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steamsync', 'steamsync.launchers']

package_data = \
{'': ['*'], 'steamsync.launchers': ['static/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'vdf>=3.3,<4.0']

entry_points = \
{'console_scripts': ['steamsync = steamsync.steamsync:main']}

setup_kwargs = {
    'name': 'steamsync',
    'version': '0.4.0',
    'description': 'Tool to automatically add games from the Epic Games Launcher to Steam',
    'long_description': 'See root readme.',
    'author': 'Jayden Milne',
    'author_email': 'jaydenmilne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jaydenmilne/steamsync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
