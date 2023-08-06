# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['har2tree']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'charset-normalizer>=2,<4',
 'ete3>=3.1.2,<4.0.0',
 'filetype>=1.2.0,<2.0.0',
 'lxml>=4.9.2,<5.0.0',
 'publicsuffixlist>=0.9.3,<0.10.0',
 'six>=1.16.0,<2.0.0',
 'w3lib>=2.1.1,<3.0.0']

extras_require = \
{':python_version < "3.10"': ['numpy==1.23.3'],
 ':python_version >= "3.10"': ['numpy>=1.23.4,<2.0.0'],
 'docs': ['Sphinx>=6.1.3,<7.0.0']}

setup_kwargs = {
    'name': 'har2tree',
    'version': '1.18.0',
    'description': 'HTTP Archive (HAR) to ETE Toolkit generator',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/har2tree/badge/?version=latest)](https://har2tree.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/Lookyloo/har2tree/branch/main/graph/badge.svg)](https://codecov.io/gh/Lookyloo/har2tree)\n\nHar2Tree\n========\n\n\nThis package generate a tree out of a HAR dump.\n\n\nInstallation\n============\n\n```bash\npip install har2tree\n```\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Lookyloo/har2tree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
