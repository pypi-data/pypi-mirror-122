# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wg_config_generator']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'attrs>=21.2.0,<22.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['wg-config-generator = wg_config_generator.main:main']}

setup_kwargs = {
    'name': 'wg-config-generator',
    'version': '0.1.0',
    'description': 'Wireguard Config Generator',
    'long_description': None,
    'author': 'Oliver Burghard',
    'author_email': 'info@oliver-burghard.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
