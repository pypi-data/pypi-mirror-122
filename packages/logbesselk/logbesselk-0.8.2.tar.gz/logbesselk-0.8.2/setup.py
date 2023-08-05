# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logbesselk']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.5,<3.0']

setup_kwargs = {
    'name': 'logbesselk',
    'version': '0.8.2',
    'description': '',
    'long_description': None,
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
