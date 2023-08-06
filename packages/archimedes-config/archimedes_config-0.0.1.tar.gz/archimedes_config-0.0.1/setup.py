# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archimedes_config']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.1,<40.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'archimedes-config',
    'version': '0.0.1',
    'description': '',
    'long_description': '# archimedes-config\n\nThis library handles config files for services used by Optimeering AS.\n',
    'author': 'BigyaPradhan',
    'author_email': 'bigya.pradhan@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
