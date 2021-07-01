from cone.tile import Tile
import json


class MapTile(Tile):
    map_id = 'map'
    map_layers = [{
        'title': 'OpenStreetMap',
        'url_template': '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'options': {
            'attribution': 'OSM map data © <a href="http://openstreetmap.org">OSM</a>',
            'minZoom': 2,
            'maxZoom': 18
        }
    }]
    map_center = [47.2688805, 11.3929127]
    map_zoom = 8
    map_marker_source = None
    map_factory = 'cone.maps.Map'

    def render(self):
        return (
            u'<div class="cone_map"'
            u'     id="{id}"'
            u'     data-map-factory="{factory}"'
            u'     data-map-layers=\'{layers}\''
            u'     data-map-center=\'{center}\''
            u'     data-map-zoom="{zoom}"'
            u'     data-map-source="{source}">'
            u'</div>'
        ).format(
            id=self.map_id,
            layers=json.dumps(self.map_layers),
            center=json.dumps(self.map_center),
            zoom=self.map_zoom,
            source=self.map_marker_source,
            factory=self.map_factory
        )
