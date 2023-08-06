# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastadmin',
 'fastadmin.api',
 'fastadmin.models',
 'fastadmin.models.orm',
 'fastadmin.schemas']

package_data = \
{'': ['*'],
 'fastadmin': ['static/css/*', 'static/images/*', 'static/js/*', 'templates/*']}

install_requires = \
['fastapi>=0.92.0,<0.93.0',
 'jinja2>=3.1.2,<4.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'fastadmin',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Seva D',
    'author_email': 'vsdudakov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vsdudakov/fastadmin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
