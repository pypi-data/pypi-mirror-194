# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkparse', 'vkparse.driver', 'vkparse.models', 'vkparse.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0']

setup_kwargs = {
    'name': 'vkparse',
    'version': '0.1.1',
    'description': 'Convert VK GDPR dumps to JSON/CSV/SQLite3',
    'long_description': None,
    'author': 'Matthew Nekirov',
    'author_email': 'matthew.nekirov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
