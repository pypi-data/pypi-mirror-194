# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simulatte',
 'simulatte.ant',
 'simulatte.buffer',
 'simulatte.demand',
 'simulatte.demand.generators',
 'simulatte.distance',
 'simulatte.events',
 'simulatte.logger',
 'simulatte.operations',
 'simulatte.picking_cell',
 'simulatte.picking_cell.areas',
 'simulatte.picking_cell.observables',
 'simulatte.picking_cell.observers',
 'simulatte.resources',
 'simulatte.service_point',
 'simulatte.simpy_extension',
 'simulatte.simpy_extension.filter_multi_store',
 'simulatte.simpy_extension.hash_store',
 'simulatte.simpy_extension.multi_store',
 'simulatte.simpy_extension.sequential_multi_store',
 'simulatte.simpy_extension.sequential_store',
 'simulatte.stores',
 'simulatte.stores.warehouse_location',
 'simulatte.system',
 'simulatte.system.managers',
 'simulatte.system.policies',
 'simulatte.timings',
 'simulatte.typings',
 'simulatte.unitload',
 'simulatte.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'pandas>=1.5.1,<2.0.0',
 'simpy>=4.0.1,<5.0.0',
 'tabulate>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'simulatte',
    'version': '0.1.1',
    'description': '',
    'long_description': '![Coverage](https://raw.githubusercontent.com/dmezzogori/simulatte/main/coverage.svg)\n',
    'author': 'Davide Mezzogori',
    'author_email': 'dmezzogori@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
