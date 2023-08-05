# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whisper_cpp_cdll']

package_data = \
{'': ['*']}

install_requires = \
['scipy==1.9.3']

setup_kwargs = {
    'name': 'whisper-cpp-cdll',
    'version': '0.0.2',
    'description': 'toolkit for whisper.cpp',
    'long_description': '# whisper.cpp.cdll\n',
    'author': 'limdongjin',
    'author_email': 'geniuslim27@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/limdongjin/whisper.cpp.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
