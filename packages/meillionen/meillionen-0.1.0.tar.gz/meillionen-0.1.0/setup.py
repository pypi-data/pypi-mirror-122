# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meillionen', 'meillionen.interface']

package_data = \
{'': ['*']}

install_requires = \
['flatbuffers>=2.0,<3.0',
 'landlab>=2.3.0,<3.0.0',
 'netCDF4>=1.5.7,<2.0.0',
 'pyarrow>=5.0.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'xarray>=0.19.0,<0.20.0']

extras_require = \
{'prefect': ['prefect>=0.15.6,<0.16.0']}

setup_kwargs = {
    'name': 'meillionen',
    'version': '0.1.0',
    'description': 'A model interface serialization and rpc framework',
    'long_description': None,
    'author': 'Calvin Pritchard',
    'author_email': 'calvin.pritchard@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
