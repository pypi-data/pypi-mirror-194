# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_rling']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'sklearn>=0.0.post1,<0.1']

setup_kwargs = {
    'name': 'package-rling',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'lingziyu',
    'author_email': 'kobelzy2020@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
