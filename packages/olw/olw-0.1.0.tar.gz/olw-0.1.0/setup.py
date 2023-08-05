# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['OLW',
 'OLW.event_management',
 'OLW.event_management.event_connector',
 'OLW.event_management.event_executer',
 'OLW.event_management.event_executer.observer',
 'OLW.event_management.event_executer.subject',
 'OLW.window',
 'OLW.window.point_manipulator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'olw',
    'version': '0.1.0',
    'description': '',
    'long_description': '# OLW\nOverLayWatch\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
