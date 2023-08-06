# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['betfair_parser',
 'betfair_parser.spec',
 'betfair_parser.spec.api',
 'betfair_parser.spec.streaming']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2022', 'msgspec>=0.12']

setup_kwargs = {
    'name': 'betfair-parser',
    'version': '0.1.19',
    'description': '',
    'long_description': 'None',
    'author': 'Bradley McElroy',
    'author_email': 'bradley.mcelroy@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
