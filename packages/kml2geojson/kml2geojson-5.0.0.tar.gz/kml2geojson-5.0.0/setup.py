# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kml2geojson']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['k2g = kml2geojson.cli:k2g']}

setup_kwargs = {
    'name': 'kml2geojson',
    'version': '5.0.0',
    'description': 'A Python library to covert KML files to GeoJSON files',
    'long_description': None,
    'author': 'Alex Raichev',
    'author_email': 'alex@raichev.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
