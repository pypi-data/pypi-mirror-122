# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynight']

package_data = \
{'': ['*']}

install_requires = \
['brish>=0.3.3,<0.4.0', 'dnspython>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'pynight',
    'version': '0.1.0',
    'description': 'My Python utility library.',
    'long_description': None,
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
