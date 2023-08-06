# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jenkins_tui', 'jenkins_tui.widgets']

package_data = \
{'': ['*']}

install_requires = \
['python-jenkins>=1.7.0,<2.0.0',
 'rich>=10.11.0,<11.0.0',
 'textual>=0.1.12,<0.2.0',
 'toml>=0.10.2,<0.11.0',
 'types-requests>=2.25.9,<3.0.0',
 'types-toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['jenkins = jenkins_tui.app:run']}

setup_kwargs = {
    'name': 'jenkins-tui',
    'version': '0.0.2',
    'description': 'An interactive TUI for Jenkins',
    'long_description': None,
    'author': 'chelnak',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chelnak/jenkins-tui',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
