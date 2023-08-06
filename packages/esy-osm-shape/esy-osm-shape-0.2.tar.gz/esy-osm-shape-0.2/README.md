# esy-osm-shape

`esy.osm.shape` is a Python library to convert
[OpenStreetMap](https://www.openstreetmap.org) primitives to
[shapely](https://shapely.readthedocs.io/en/latest/) objects.

## Usage

The following examples operate on a historic dataset for Andorra from
[geofabrik](https://www.geofabrik.de/). Let's download the dataset first:

```python
>>> import urllib.request
>>> filename, headers = urllib.request.urlretrieve(
...     'https://download.geofabrik.de/europe/andorra-190101.osm.pbf',
...     filename='andorra.osm.pbf'
... )

```

Open the file and generate linestrings for each *highway* OpenStreetMap entry.

```python
>>> import shapely, esy.osm.shape
>>> shape = esy.osm.shape.Shape('andorra.osm.pbf')
>>> highways = [
...     shape for shape, id, tags in shape(lambda e: e.tags.get('highway'))
...     if type(shape) is shapely.geometry.LineString
... ]

```

Using shapely objects it is also easy to compute geometric properties, like for
example the length of the highways (note that the unit of this length is in
longitude and latitude):

```python
>>> sum(linestring.length for linestring in highways)
16.952160743015657

```

For slightly more details, jump to the
[documentation](https://dlr-ve-esy.gitlab.io/esy-osm-shape).
