# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['releasy']

package_data = \
{'': ['*']}

install_requires = \
['pygit2>=1.11.1,<2.0.0', 'python-dateutil>=2.8.2,<3.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'releasy-lib',
    'version': '4.2.1',
    'description': 'A library to mine release data',
    'long_description': 'Releasy\n=======\n\n[![Build Status](https://github.com/gems-uff/releasy/actions/workflows/pytest.yml/badge.svg)](https://github.com/gems-uff/releasy/actions/workflows/pytest.yml)\n\nReleasy is a tool that collects provenance data from releases \nby parsing the software version control and issue tracking\nsystems.\n\nPapers\n======\n\n[Curty, F., Kohwalter, T., Braganholo, V., Murta, L., 2018. An Infrastructure for Software Release Analysis through Provenance Graphs. Presented at the VI Workshop on Software Visualization, Evolution and Maintenance.](https://goo.gl/9u8rzc)\n\n',
    'author': 'Felipe Curty',
    'author_email': 'felipecrp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gems-uff/releasy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
