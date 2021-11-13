from cone.app import cfg
from cone.app import main_hook
from cone.maps.browser import static_resources
import logging


logger = logging.getLogger('cone.maps')


@main_hook
def initialize_maps(config, global_config, settings):
    # application startup initialization

    # ignore yafowil leaflet dependencies if cone.maps is installed
    cfg.yafowil.js_skip.add('yafowil.widget.location.dependencies')
    cfg.yafowil.css_skip.add('yafowil.widget.location.dependencies')

    # protected CSS
    cfg.css.protected.append('maps-static/leaflet/leaflet.css')
    cfg.css.protected.append('maps-static/leaflet-geosearch/geosearch.css')

    # protected JS
    cfg.js.protected.append('maps-static/leaflet/leaflet.js')
    cfg.js.protected.append('maps-static/leaflet-nogap/L.TileLayer.NoGap.js')
    cfg.js.protected.append('maps-static/leaflet-geosearch/geosearch.umd.js')
    cfg.js.protected.append('maps-static/cone.maps.js')

    # add translation
    config.add_translation_dirs('cone.maps:locale/')

    # static resources
    config.add_view(static_resources, name='maps-static')

    # scan browser package
    config.scan('cone.maps.browser')
