from cone.tile import Tile
import json


class MapTile(Tile):
    """Tile rendering a leaflet map.

    Reference: https://leafletjs.com/reference.html
    """

    map_factory = 'cone_maps.Map'
    """Factory used for map creation in Javascript.

    The definded factory must accept the map related DOM element as argument
    and is responsible to initialize the leaflet map.

    It points to a class or function and does property lookup on window with
    '.' as delimiter, e.g:

        'cone_maps.Map'

    corresponds to:

        cone_maps: {
            Map: {}
        }

    If JS map factory needs to be customized, this is usually done by subclassing
    'cone_maps.Map':

        my_namespace = {};

        my_namespace.Map = class extends cone_maps.Map {
            constructor(elem) {
                elem.height(800);
                super(elem);
            }
        }
    """

    map_id = 'map'
    """HTML id of the map."""

    map_css = 'cone-map'
    """CSS class of the map element.

    The default JS map implementation searches for
    for all `div` elements with `cone-map` CSS class set and initializes map
    instances for them.

    If it's desired to completly customize map instancing on client side, this
    property must be changed.
    """

    map_options = {}
    """Map options passed to the leaflet map constructor.

    See: https://leafletjs.com/reference.html#map-l-map
    """

    map_control_options = {}
    """Layers control options passed to the leaflet layers control constructor.

    See: https://leafletjs.com/reference.html#control-layers
    """

    map_layers = [{
        # general layer options
        'factory': 'tile_layer',   # layer factory
        'category': 'base',        # base|overlay
        'display': True,           # initial display
        'title': 'OpenStreetMap',  # layer title
        # factory specific layer options
        'urlTemplate': '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'options': {
            'attribution': 'OSM map data © <a href="http://openstreetmap.org">OSM</a>',
            'minZoom': 2,
            'maxZoom': 18
        }
    }]
    """List of map layer definitions.

    See: https://leafletjs.com/reference.html
    """

    map_center = [47.2688805, 11.3929127]
    """The default (initial) center of the map as lat/lng."""

    map_zoom = 8
    """The default (initial) zoom level of the map."""

    map_bounds = []
    """A list of geo points. If set, bounds take precedence over ``map_center``
    and ``map_zoom`` and the map gets positioned to fit the bounds."""

    map_markers = []
    """List of map markers to display.

    A map marker is represented by a dict like so:

        {
            'latlng': {
                'lat': 47.2688805,
                'lng': 11.3929127
            },
            'options': {
                'title': 'Marker Tile'
            },
            'popup': {
                'content': '<div>Marker Popup</div>',
                'options': {
                    'keepInView': True
                }
            }
        }

    For available marker options,
    see https://leafletjs.com/reference.html#marker

    For available popup options,
    see https://leafletjs.com/reference.html#popup-option
    """

    map_markers_source = ''
    """JSON endpoint to fetch markers from. For details about the expected
    format, see ``map_markers``.
    """

    map_marker_groups = []
    """List of map marker groups to display.

    Not implemented in JS yet.
    """

    map_marker_groups_source = ''
    """JSON endpoint to fetch marker groups from.

    Not implemented in JS yet.
    """

    def render(self):
        settings = dict(
            factory=self.map_factory,
            options=self.map_options,
            control_options=self.map_control_options,
            layers=self.map_layers,
            center=self.map_center,
            zoom=self.map_zoom,
            bounds=self.map_bounds,
            markers=self.map_markers,
            markers_source=self.map_markers_source,
            groups=self.map_marker_groups,
            groups_source=self.map_marker_groups_source
        )
        return (
            u'<div class="{css}"'
            u'     id="{id}"'
            u'     data-map-settings=\'{settings}\' >'
            u'</div>'
        ).format(
            css=self.map_css,
            id=self.map_id,
            settings=json.dumps(settings)
        )
