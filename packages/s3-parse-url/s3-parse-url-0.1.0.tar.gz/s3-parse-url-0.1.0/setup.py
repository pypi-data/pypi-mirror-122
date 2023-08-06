# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s3_parse_url', 's3_parse_url.ext', 's3_parse_url.storages']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 's3-parse-url',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
