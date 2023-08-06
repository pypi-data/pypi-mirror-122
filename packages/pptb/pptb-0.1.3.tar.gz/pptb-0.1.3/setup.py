# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pptb',
 'pptb.nn',
 'pptb.optimizer',
 'pptb.tools',
 'pptb.vision',
 'pptb.vision.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pptb',
    'version': '0.1.3',
    'description': '🚣 一些常用的但 paddle 里没有的小工具～',
    'long_description': None,
    'author': 'Nyakku Shigure',
    'author_email': 'sigure.qaq@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
