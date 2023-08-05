# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_requirements_export']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.3.2,<2.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'poetry.application.plugin': ['simple-requirements = '
                               'simple_requirements_export.plugin:SimpleRequirementsExportPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-simple-requirements-export',
    'version': '0.1.0',
    'description': 'A different way to export your poetry requirements as a requirements.txt file',
    'long_description': 'None',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
