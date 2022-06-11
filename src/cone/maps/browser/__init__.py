from cone.app.browser.resources import resources
from cone.app.browser.resources import set_resource_include
import webresource as wr
import os


resources_dir = os.path.join(os.path.dirname(__file__), 'static')


# leaflet core
leaflet_resources = wr.ResourceGroup(
    name='cone.maps-leaflet',
    directory=os.path.join(resources_dir, 'leaflet'),
    path='leaflet',
    group=resources
)
leaflet_resources.add(wr.ScriptResource(
    name='leaflet-js',
    resource='leaflet-src.js',
    compressed='leaflet.js'
))
leaflet_resources.add(wr.StyleResource(
    name='leaflet-css',
    resource='leaflet.css'
))

# Leaflet.TileLayer.NoGap
leaflet_nogap_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-nogap',
    directory=os.path.join(resources_dir, 'leaflet-nogap'),
    path='leaflet-nogap',
    group=resources
)
leaflet_nogap_resources.add(wr.ScriptResource(
    name='leaflet-nogap-js',
    depends='leaflet-js',
    resource='L.TileLayer.NoGap.js'
))

# leaflet-geosearch
leaflet_geosearch_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-geosearch',
    directory=os.path.join(resources_dir, 'leaflet-geosearch'),
    path='leaflet-geosearch',
    group=resources
)
leaflet_geosearch_resources.add(wr.ScriptResource(
    name='leaflet-geosearch-js',
    depends='leaflet-js',
    resource='geosearch.umd.js'
))
leaflet_geosearch_resources.add(wr.StyleResource(
    name='leaflet-geosearch-css',
    depends='leaflet-css',
    resource='geosearch.css'
))

# Leaflet.markercluster
leaflet_markercluster_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-markercluster',
    directory=os.path.join(resources_dir, 'leaflet-markercluster'),
    path='leaflet-markercluster',
    group=resources
)
leaflet_markercluster_resources.add(wr.ScriptResource(
    name='leaflet-markercluster-js',
    depends='leaflet-js',
    resource='leaflet.markercluster-src.js',
    compressed='leaflet.markercluster.js'
))
leaflet_markercluster_resources.add(wr.StyleResource(
    name='leaflet-markercluster-css',
    depends='leaflet-css',
    resource='MarkerCluster.css'
))
leaflet_markercluster_resources.add(wr.StyleResource(
    name='leaflet-markercluster-default-css',
    depends='leaflet-markercluster-css',
    resource='MarkerCluster.Default.css'
))

# Leaflet-active-area
leaflet_activearea_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-activearea',
    directory=os.path.join(resources_dir, 'leaflet-activearea'),
    path='leaflet-activearea',
    group=resources
)
leaflet_activearea_resources.add(wr.ScriptResource(
    name='leaflet-activearea-js',
    depends='leaflet-js',
    resource='leaflet.activearea.js'
))

# proj4js
proj4_resources = wr.ResourceGroup(
    name='cone.maps-proj4',
    directory=os.path.join(resources_dir, 'proj4js'),
    path='proj4js',
    group=resources
)
proj4_resources.add(wr.ScriptResource(
    name='proj4-js',
    resource='proj4-src.js',
    compressed='proj4.js'
))

# Proj4Leaflet
leaflet_proj4_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-proj4',
    directory=os.path.join(resources_dir, 'leaflet-proj4'),
    path='leaflet-proj4',
    group=resources
)
leaflet_proj4_resources.add(wr.ScriptResource(
    name='leaflet-proj4-js',
    depends=['leaflet-js', 'proj4-js'],
    resource='proj4leaflet.js'
))

# cone maps
cone_maps_resources = wr.ResourceGroup(
    name='cone.maps-maps',
    directory=os.path.join(resources_dir, 'maps'),
    path='maps',
    group=resources
)
cone_maps_resources.add(wr.ScriptResource(
    name='cone-maps-js',
    depends='leaflet-js',
    resource='cone.maps.js',
    compressed='cone.maps.min.js'
))


def configure_resources(settings):
    def included(name):
        return settings.get(name, 'false') == 'true'

    include = True if included('cone.maps.public') else 'authenticated'

    # leaflet core
    set_resource_include(settings, 'leaflet-js', include)
    set_resource_include(settings, 'leaflet-css', include)

    # Leaflet.TileLayer.NoGap
    nogap_include = include if included('cone.maps.nogap') else False
    set_resource_include(settings, 'leaflet-nogap-js', nogap_include)

    # leaflet-geosearch
    geosearch_include = include if included('cone.maps.geosearch') else False
    set_resource_include(settings, 'leaflet-geosearch-js', geosearch_include)
    set_resource_include(settings, 'leaflet-geosearch-css', geosearch_include)

    # Leaflet.markercluster
    mc_include = include if included('cone.maps.markercluster') else False
    set_resource_include(settings, 'leaflet-markercluster-js', mc_include)
    set_resource_include(settings, 'leaflet-markercluster-css', mc_include)
    set_resource_include(settings, 'leaflet-markercluster-default-css', mc_include)

    # Leaflet-active-area
    activearea_include = include if included('cone.maps.activearea') else False
    set_resource_include(settings, 'leaflet-activearea-js', activearea_include)

    # proj4js and Proj4Leaflet
    proj4_include = include if included('cone.maps.proj4') else False
    set_resource_include(settings, 'proj4-js', proj4_include)
    set_resource_include(settings, 'leaflet-proj4-js', proj4_include)

    # cone maps
    set_resource_include(settings, 'cone-maps-js', include)
