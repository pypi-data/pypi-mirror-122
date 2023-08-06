# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojsonhash']

package_data = \
{'': ['*']}

install_requires = \
['pygeohash>=1.2.0']

setup_kwargs = {
    'name': 'geojsonhash',
    'version': '0.1.1',
    'description': 'README',
    'long_description': '# geojsonhash\n\n![CI](https://github.com/AdrianSeguraOrtiz/geojsonhash/actions/workflows/ci.yml/badge.svg)\n![Release](https://github.com/AdrianSeguraOrtiz/geojsonhash/actions/workflows/release.yml/badge.svg)\n![Pypi](https://img.shields.io/pypi/v/geojsonhash)\n![License](https://img.shields.io/apm/l/geojsonhash)\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\nThis package is responsible for generating identifiers for geojson objects. To do so, it makes use of the pygeohash library in charge of generating the identifiers of the different points contained in the geojson.\n\nIn this implementation, individual points are ignored, treating the input geojson as a set of polygons defining a surface. The polygons are sorted according to their coordinates while the northwest-most vertex of the polygons defines the starting point for encoding. \n\n## Installation\n\nTo install the package there are two options: through poetry or by using the pip command\n\n### Pip command\n\n```bash\n$ pip install geojsonhash\n```\n\n### Poetry\n\n```bash\n$ git clone https://github.com/AdrianSeguraOrtiz/geojsonhash.git\n$ cd geojsonhash\n$ poetry install\n```\n\n## Example\n\nAn example is shown below:\n\n```python\nfrom geojsonhash import get_geojson_id\nimport json\n\nwith open("./resources/geojson.json") as geo_d:\n    geojson = json.load(geo_d)\n\ngeojson_id = get_geojson_id(geojson)\nprint(geojson_id)\n```\n\nTo run it through console we can do:\n\n```bash\n$ cd examples\n$ python example.py\n```',
    'author': 'Adrián Segura Ortiz',
    'author_email': 'adrianseor.99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AdrianSeguraOrtiz/geojsonhash/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
