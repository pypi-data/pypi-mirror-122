# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypanzer', 'pypanzer.tools']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.9,<2.0.0',
 'emoji>=1.2.0,<2.0.0',
 'loguru>=0.4.1,<0.5.0',
 'pandas==1.1.5',
 'pymongo>=3.9.0,<4.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.22.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'pypanzer',
    'version': '1.0.3',
    'description': 'panzer tools for python language',
    'long_description': None,
    'author': '于中华',
    'author_email': '583512498@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
