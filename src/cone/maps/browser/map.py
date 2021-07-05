from cone.tile import Tile
import json


class MapTile(Tile):
    """Tile rendering a leaflet map.

    Reference: https://leafletjs.com/reference-1.7.1.html
    """

    map_factory = 'cone.maps.Map'
    """Factory used for map creation in Javascript.

    The definded factory must accept the map related DOM element as argument
    and is responsible to initialize the leaflet map.

    It points to a class or function and does property lookup on window with
    '.' as delimiter, e.g:

        'cone.maps.Map'

    corresponds to:

        cone: {
            maps: {
                Map: {}
            }
        }

    If JS map factory needs to be customized, this is usually done by subclassing
    'cone.maps.Map':

        my_namespace = {};

        my_namespace.Map = class extends cone.maps.Map {
            constructor(elem) {
                elem.height(800);
                super(elem);
            }
        }
    """

    map_id = 'map'
    """HTML id of the map.
    """

    map_options = None
    """Map options passed to the leaflet map constructor.

    See: https://leafletjs.com/reference-1.7.1.html#map-l-map
    """

    map_layers = [{
        'title': 'OpenStreetMap',
        'url_template': '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'options': {
            'attribution': 'OSM map data © <a href="http://openstreetmap.org">OSM</a>',
            'minZoom': 2,
            'maxZoom': 18
        }
    }]
    """List of map layer definitions. Each layer definition consists of a title,
    the URL template and the layer options passed to leaflet layer constructor.

    See: https://leafletjs.com/reference-1.7.1.html#tilelayer-l-tilelayer
    """

    map_center = [47.2688805, 11.3929127]
    """The default (initial) center of the map as lat/lng.
    """

    map_zoom = 8
    """The default (initial) zoom level of the map
    """

    map_marker_source = None

    def render(self):
        return (
            u'<div class="cone_map"'
            u'     id="{id}"'
            u'     data-map-factory="{factory}"'
            u'     data-map-options=\'{options}\''
            u'     data-map-layers=\'{layers}\''
            u'     data-map-center=\'{center}\''
            u'     data-map-zoom="{zoom}"'
            u'     data-map-source="{source}">'
            u'</div>'
        ).format(
            id=self.map_id,
            factory=self.map_factory,
            options=json.dumps(self.map_options),
            layers=json.dumps(self.map_layers),
            center=json.dumps(self.map_center),
            zoom=self.map_zoom,
            source=self.map_marker_source
        )
