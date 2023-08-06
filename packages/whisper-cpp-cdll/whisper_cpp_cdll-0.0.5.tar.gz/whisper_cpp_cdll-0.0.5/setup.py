# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whisper_cpp_cdll']

package_data = \
{'': ['*']}

install_requires = \
['scipy>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'whisper-cpp-cdll',
    'version': '0.0.5',
    'description': 'toolkit for whisper.cpp',
    'long_description': "# whisper.cpp.cdll\n\n## Quick Start\n\n**1. Install whisper.cpp**\n```bash\ngit clone https://github.com/ggerganov/whisper.cpp\n\ncd whisper.cpp\nmake tiny\nmake libwhisper.so\n```\n\n**2. Install whisper_cpp_cdll**\n```bash\npip install whisper_cpp_cdll\n```\n\n**3. Usage**\n```python3\nfrom whisper_cpp_cdll.core import run_whisper\nfrom whisper_cpp_cdll.util import read_audio\n\n# your whisper.cpp files path\nlibname = './whisper.cpp/libwhisper.so'\nfname_model = './whisper.cpp/models/ggml-tiny.bin'\nd = read_audio('./whisper.cpp/samples/jfk.wav')\n\nresult = run_whisper(data = d, libname = libname, fname_model = fname_model, language=b'en')\n#=> [{'segment_id': 0, 'text': ' And so my fellow Americans ask not what your country can do for you ask what you can do for your country.', 'start': 0, 'end': 176000, 'tokens': [{..}]},..... ]\n```\n",
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
