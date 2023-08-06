# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetchers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'fetchers',
    'version': '0.1.0',
    'description': 'Website Scraper',
    'long_description': None,
    'author': 'imjuanleonard',
    'author_email': 'julioanthonyleonard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
