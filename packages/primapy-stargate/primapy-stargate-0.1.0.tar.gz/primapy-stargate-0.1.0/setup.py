# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['primapy_stargate',
 'primapy_stargate.hub',
 'primapy_stargate.model',
 'primapy_stargate.oracle']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.68.1,<0.69.0', 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'primapy-stargate',
    'version': '0.1.0',
    'description': 'Hub for Oracles',
    'long_description': None,
    'author': 'Team AMOps',
    'author_email': 'amops@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
