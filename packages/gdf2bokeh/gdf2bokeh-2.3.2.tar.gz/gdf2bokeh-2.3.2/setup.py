# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdf2bokeh', 'gdf2bokeh.helpers']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=3.0.3,<4.0.0', 'geopandas>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'gdf2bokeh',
    'version': '2.3.2',
    'description': 'An easy way to map geodataframes on bokeh',
    'long_description': '# gdf2bokeh\nAn easy way to map your geographic data (from a GeoDataFrame) with [bokeh >=__2.3__](https://github.com/bokeh/bokeh/tree/2.3)\nBecause it\'s boring to convert shapely geometry to bokeh format !!\n\n![CI](https://github.com/amauryval/gdf2bokeh/workflows/CI/badge.svg)\n[![codecov](https://codecov.io/gh/amauryval/gdf2bokeh/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/gdf2bokeh)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/version.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/latest_release_date.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/platforms.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/installer/conda.svg)](https://conda.anaconda.org/amauryval)\n\n\n## How to install the conda package ?\n\n### With Anaconda\n\n```bash\nconda install -c amauryval gdf2bokeh\n```\n\n### with pip\n\n```bash\npip install gdf2bokeh\n```\n\n\n## How to use it ?!\n\nA small example :\n\nCheck bokeh documentation in order to style your data :\n    \n* [bokeh marker style options](https://docs.bokeh.org/en/latest/docs/reference/models/markers.html) to style point features\n* [bokeh multi_line style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_line) to style LineString and MultiLineString features\n* [bokeh multi_polygon style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_polygons) to style polygon and multipolygons features\n\n```python\nfrom bokeh.plotting import show\nimport geopandas as gpd\nfrom gdf2bokeh import Gdf2Bokeh\n\nlayers_to_add = [\n    {\n        "input_gdf": gpd.GeoDataFrame.from_file("your_geo_layer.geojson"),\n        "legend": "My beautiful layer",  # required, can be the name of an column name (from your input gdf)\n        "fill_color": "orange",  # here we found one argument use by bokeh to style your layer. Take care about geometry type\n    },\n    {\n        "input_wkt": "LINESTRING(0 0, 25 25)",  # you can add an input wkt\n        "legend": "My beautiful layer",  # required\n        "color": "orange",  # here we found one argument use by bokeh to style your layer. Take care about geometry type\n    }\n]\n# Points, LineString, MultiLineString, Polygons (+ holes) and MultiPolygons (+ holes) are supported\n\nmy_map = Gdf2Bokeh(\n    "My beautiful map",  # required: map title\n    width=800,  # optional: figure width, default 800\n    height=600,  # optional: figure width, default 600\n    x_range=None,  # optional: x_range, default None\n    y_range=None,  # optional: y_range, default None\n    background_map_name="CARTODBPOSITRON",  # optional: background map name, default: CARTODBPOSITRON\n    layers=layers_to_add    # optional: bokeh layer to add from a list of dict contains geodataframe settings, see dict above\n)\n# to get all the bokeh layer containers (dict), in order to update them (interactivity, slider... on a bokeh serve)\nbokeh_layer_containers = my_map.get_bokeh_layer_containers\n\nshow(my_map.figure)\n```\n\n\nAlso, you can find a bokeh serve example with a slider widget.\nOn the terminal, run :\n\n```bash\nbokeh serve --show bokeh_serve_example.py\n```\n',
    'author': 'amauryval',
    'author_email': 'amauryval@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
