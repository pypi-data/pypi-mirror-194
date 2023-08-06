# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_eventdone']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-rc.3,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-eventdone',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Padro Felice',
    'author_email': '2659737583@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
