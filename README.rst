.. image:: https://img.shields.io/pypi/v/cone.maps.svg
    :target: https://pypi.python.org/pypi/cone.maps
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/cone.maps.svg
    :target: https://pypi.python.org/pypi/cone.maps
    :alt: Number of PyPI downloads

.. image:: https://github.com/conestack/cone.maps/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/conestack/cone.maps/actions/workflows/python-package.yml
    :alt: Package build

.. image:: https://coveralls.io/repos/github/bluedynamics/cone.maps/badge.svg?branch=master
    :target: https://coveralls.io/github/bluedynamics/cone.maps?branch=master


This package provides maps integration in to cone.app.
It utilizes `Leaflet JS <https://leafletjs.com/>`_.

Currently, version `v1.7.1 <https://github.com/Leaflet/Leaflet/releases>_` is
included.

For avoiding 1px gap between tiles,
`Leaflet.TileLayer.NoGap <https://github.com/Leaflet/Leaflet.TileLayer.NoGap>`_
is included.

For geocoding,
`leaflet-geosearch <https://smeijer.github.io/leaflet-geosearch>`_ (3.5.0)
is included.

For grouping of map markers,
`Leaflet.markercluster <https://github.com/Leaflet/Leaflet.markercluster>`_
(1.5.3) is included.

For defining active map area, e.g. if parts of a map is used as background,
`Leaflet-active-area <https://github.com/Mappy/Leaflet-active-area>`_ is
included. Currenlty the source is taken from
`this <https://github.com/rnixx/Leaflet-active-area/tree/leaflet-1.7.1-compat>`_
fork, which includes updates for Leaflet 1.7.1.


Contributors
============

- Robert Niederreiter
