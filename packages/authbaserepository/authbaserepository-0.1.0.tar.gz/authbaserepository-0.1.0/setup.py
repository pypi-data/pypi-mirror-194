# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authbaserepository',
 'authbaserepository.auth_middleweare',
 'authbaserepository.base_repo']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-jwt-auth>=0.5.0,<0.6.0', 'sqlalchemy==1.4.41']

setup_kwargs = {
    'name': 'authbaserepository',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
