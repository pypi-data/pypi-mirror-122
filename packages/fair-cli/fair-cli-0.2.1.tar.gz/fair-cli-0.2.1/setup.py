# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fair', 'fair.parsing', 'fair.registry', 'fair.templates']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.0,<9.0.0',
 'requests>=2.23.0,<3.0.0',
 'rich>=10.2.2,<11.0.0',
 'semver>=2.13.0,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['fair = fair.cli:cli']}

setup_kwargs = {
    'name': 'fair-cli',
    'version': '0.2.1',
    'description': 'Synchronization interface for the SCRC FAIR Data Pipeline registry',
    'long_description': None,
    'author': 'Nathan Cummings',
    'author_email': 'nathan.cummings@ukaea.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
