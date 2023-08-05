# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['findmi']

package_data = \
{'': ['*']}

install_requires = \
['micloud>=0.6,<0.7', 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['findmi = findmi.main:main']}

setup_kwargs = {
    'name': 'findmi',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'thewh1teagle',
    'author_email': '61390950+thewh1teagle@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
