# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['navig8r']

package_data = \
{'': ['*'], 'navig8r': ['images/*']}

install_requires = \
['discord.py>=2.1.0,<3.0.0',
 'gspread>=5.7.1,<6.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['navig8r = navig8r.navig8r:app']}

setup_kwargs = {
    'name': 'navig8r',
    'version': '0.1.3',
    'description': 'A discord bot for students that supplies them with resources and grade reports on demand.',
    'long_description': 'None',
    'author': 'Aidan Neeson, Jeff Normile, Gregory Kapfhammer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.6,<4.0',
}


setup(**setup_kwargs)
