# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shec']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'httpx[brotli,http2]>=0.19.0,<0.20.0',
 'tenacity>=8.0.1,<9.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'shec',
    'version': '0.0.0',
    'description': 'An unofficial Splunk HTTP Endpoint Collector client (and more).',
    'long_description': 'None',
    'author': 'Mark Beacom',
    'author_email': 'm@beacom.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
