# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmmate', 'kmmate.generate', 'kmmate.utils']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['kmmate = kmmate.cli:app']}

setup_kwargs = {
    'name': 'kmmate',
    'version': '0.1.0',
    'description': 'The awesome tool for creating KMM projects.',
    'long_description': '# Awesome tool for working on KMM projects\n\n## Features\n\n1. Creating new project with template\n2. Fast rename shared module\n3. Fast rename package\n4. Generating components (Decompose)\n5. Generating empty features (components, data layer, domain entities)\n',
    'author': 'Artem Skopincev',
    'author_email': 'sckopincev.artyom@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
