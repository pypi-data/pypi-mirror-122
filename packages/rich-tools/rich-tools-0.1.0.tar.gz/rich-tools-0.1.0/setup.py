# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'rich>=10.12.0,<11.0.0']

setup_kwargs = {
    'name': 'rich-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Avi Perl',
    'author_email': 'avi@aviperl.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
