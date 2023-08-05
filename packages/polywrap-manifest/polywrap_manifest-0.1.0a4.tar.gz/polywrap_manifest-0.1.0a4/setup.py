# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_manifest']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-msgpack==0.1.0a4',
 'polywrap-result==0.1.0a4',
 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'polywrap-manifest',
    'version': '0.1.0a4',
    'description': 'WRAP manifest',
    'long_description': '',
    'author': 'Niraj',
    'author_email': 'niraj@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
