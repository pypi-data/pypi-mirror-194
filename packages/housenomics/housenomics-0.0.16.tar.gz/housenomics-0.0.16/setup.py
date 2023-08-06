# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'housenomics': 'src/housenomics',
 'housenomics.application': 'src/housenomics/application',
 'housenomics.application.views': 'src/housenomics/application/views',
 'housenomics.infrastructure': 'src/housenomics/infrastructure',
 'housenomics.ui.cli': 'src/housenomics/ui/cli'}

packages = \
['housenomics',
 'housenomics.application',
 'housenomics.application.views',
 'housenomics.infrastructure',
 'housenomics.ui.cli',
 'toolbox']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'rich>=13.3.1,<14.0.0',
 'sqlalchemy>=2.0.4,<3.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['housenomics = '
                     'housenomics.ui.cli.main:housenomics_cli.app']}

setup_kwargs = {
    'name': 'housenomics',
    'version': '0.0.16',
    'description': 'Manage your personal finances',
    'long_description': 'None',
    'author': 'Luís Miranda',
    'author_email': 'luistm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.11.1',
}


setup(**setup_kwargs)
