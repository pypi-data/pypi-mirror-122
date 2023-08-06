# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kbfs_upload']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'pykeybase>=0.5.0,<0.6.0',
 'python-dotenv>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['kbfsu = kbfs_upload:main']}

setup_kwargs = {
    'name': 'kbfs-upload',
    'version': '0.1.0',
    'description': 'An API for uploading files/notes to a KBFS folder',
    'long_description': None,
    'author': 'Dakota Brown',
    'author_email': 'dakota.kae.brown@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
