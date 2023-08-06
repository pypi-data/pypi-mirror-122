# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volttron',
 'volttron.router',
 'volttron.server',
 'volttron.services.auth',
 'volttron.services.config_store',
 'volttron.services.control',
 'volttron.services.external',
 'volttron.services.health',
 'volttron.services.peer',
 'volttron.services.pubsub',
 'volttron.services.routing']

package_data = \
{'': ['*']}

install_requires = \
['volttron-client>=0.3.0,<0.4.0', 'wheel>=0.36,<0.37']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['volttron = volttron.server.__main__:main']}

setup_kwargs = {
    'name': 'volttron-server',
    'version': '0.1.1',
    'description': 'Server component for VOLTTRON',
    'long_description': None,
    'author': 'C. Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
