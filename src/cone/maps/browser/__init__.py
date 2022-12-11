import webresource as wr
import os


resources_dir = os.path.join(os.path.dirname(__file__), 'static')


# leaflet core
leaflet_resources = wr.ResourceGroup(
    name='cone.maps-leaflet',
    directory=os.path.join(resources_dir, 'leaflet'),
    path='leaflet'
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
    path='leaflet-nogap'
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
    path='leaflet-geosearch'
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
    path='leaflet-markercluster'
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

# Leaflet.Editable
leaflet_editable_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-editable',
    directory=os.path.join(resources_dir, 'leaflet-editable'),
    path='leaflet-editable'
)
leaflet_editable_resources.add(wr.ScriptResource(
    name='leaflet-editable-js',
    depends='leaflet-js',
    resource='Leaflet.Editable.js'
))

# Leaflet-active-area
leaflet_activearea_resources = wr.ResourceGroup(
    name='cone.maps-leaflet-activearea',
    directory=os.path.join(resources_dir, 'leaflet-activearea'),
    path='leaflet-activearea'
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
    path='proj4js'
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
    path='leaflet-proj4'
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
    path='maps'
)
cone_maps_resources.add(wr.ScriptResource(
    name='cone-maps-js',
    depends='leaflet-js',
    resource='cone.maps.js',
    compressed='cone.maps.min.js'
))


def configure_resources(config, settings):
    def included(name):
        return settings.get(name, 'false') == 'true'

    include = True if included('cone.maps.public') else 'authenticated'

    # leaflet core
    config.register_resource(leaflet_resources)
    config.set_resource_include('leaflet-js', include)
    config.set_resource_include('leaflet-css', include)

    # Leaflet.TileLayer.NoGap
    config.register_resource(leaflet_nogap_resources)
    nogap_include = include if included('cone.maps.nogap') else False
    config.set_resource_include('leaflet-nogap-js', nogap_include)

    # leaflet-geosearch
    config.register_resource(leaflet_geosearch_resources)
    geosearch_include = include if included('cone.maps.geosearch') else False
    config.set_resource_include('leaflet-geosearch-js', geosearch_include)
    config.set_resource_include('leaflet-geosearch-css', geosearch_include)

    # Leaflet.markercluster
    config.register_resource(leaflet_markercluster_resources)
    mc_include = include if included('cone.maps.markercluster') else False
    config.set_resource_include('leaflet-markercluster-js', mc_include)
    config.set_resource_include('leaflet-markercluster-css', mc_include)
    config.set_resource_include('leaflet-markercluster-default-css', mc_include)

    # Leaflet.Editable
    config.register_resource(leaflet_editable_resources)
    editable_include = include if included('cone.maps.editable') else False
    config.set_resource_include('leaflet-editable-js', editable_include)

    # Leaflet-active-area
    config.register_resource(leaflet_activearea_resources)
    activearea_include = include if included('cone.maps.activearea') else False
    config.set_resource_include('leaflet-activearea-js', activearea_include)

    # proj4js and Proj4Leaflet
    config.register_resource(proj4_resources)
    config.register_resource(leaflet_proj4_resources)
    proj4_include = include if included('cone.maps.proj4') else False
    config.set_resource_include('proj4-js', proj4_include)
    config.set_resource_include('leaflet-proj4-js', proj4_include)

    # cone maps
    config.register_resource(cone_maps_resources)
    config.set_resource_include('cone-maps-js', include)
