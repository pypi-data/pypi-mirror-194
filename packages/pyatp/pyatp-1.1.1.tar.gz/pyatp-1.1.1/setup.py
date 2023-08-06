# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['atp',
 'atp.huggingface',
 'atp.pretrain',
 'atp.pretrain.av2vec',
 'atp.pretrain.voice2vec',
 'atp.utils']

package_data = \
{'': ['*']}

install_requires = \
['jsonpath_rw>=1.4.0', 'requests>=2.26.0']

setup_kwargs = {
    'name': 'pyatp',
    'version': '1.1.1',
    'description': 'an sdk for iflytek atp',
    'long_description': None,
    'author': 'ybyang',
    'author_email': 'ybyang7@iflytek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
