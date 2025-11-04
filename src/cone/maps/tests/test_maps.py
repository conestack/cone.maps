from cone.app import testing
from cone.app.browser import resources
from cone.app.model import BaseNode
from cone.maps import browser
from cone.maps.browser.map import MapTile
from cone.tile.tests import TileTestCase
import os
import sys
import unittest


class MapsLayer(testing.Security):

    def make_app(self, **kw):
        super(MapsLayer, self).make_app(**{
            'cone.plugins': 'cone.maps'
        })


maps_layer = MapsLayer()


class TestMapsTile(TileTestCase):
    layer = maps_layer

    def test_map_tile(self):
        model = BaseNode(name='map')
        request = self.layer.new_request()

        map_tile = MapTile()
        res = map_tile(model, request)

        self.assertTrue(res.find('class="cone-map"') > -1)
        self.assertTrue(res.find('id="map"') > -1)
        self.assertTrue(res.find('data-map-settings=') > -1)
        self.assertTrue(res.find('"factory": "cone_maps.Map"') > -1)
        self.assertTrue(res.find('"options": {') > -1)
        self.assertTrue(res.find('"control_options": {') > -1)
        self.assertTrue(res.find('"layers": [') > -1)
        self.assertTrue(res.find('"center": [') > -1)
        self.assertTrue(res.find('"zoom": 8') > -1)
        self.assertTrue(res.find('"bounds": []') > -1)
        self.assertTrue(res.find('"markers": []') > -1)
        self.assertTrue(res.find('"markers_source": ""') > -1)
        self.assertTrue(res.find('"groups": []') > -1)
        self.assertTrue(res.find('"groups_source": ""') > -1)


def np(path):
    return path.replace('/', os.path.sep)


class TestResources(unittest.TestCase):
    layer = maps_layer

    def test_leaflet_resources(self):
        resources_ = browser.leaflet_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet')
        self.assertEqual(resources_.path, 'leaflet')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet')))
        self.assertEqual(scripts[0].path, 'leaflet')
        self.assertEqual(scripts[0].file_name, 'leaflet.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(styles[0].directory.endswith(np('/static/leaflet')))
        self.assertEqual(styles[0].path, 'leaflet')
        self.assertEqual(styles[0].file_name, 'leaflet.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

    def test_leaflet_nogap_resources(self):
        resources_ = browser.leaflet_nogap_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-nogap')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-nogap')
        self.assertEqual(resources_.path, 'leaflet-nogap')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-nogap')))
        self.assertEqual(scripts[0].path, 'leaflet-nogap')
        self.assertEqual(scripts[0].file_name, 'L.TileLayer.NoGap.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_leaflet_geosearch_resources(self):
        resources_ = browser.leaflet_geosearch_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-geosearch')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-geosearch')
        self.assertEqual(resources_.path, 'leaflet-geosearch')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-geosearch')))
        self.assertEqual(scripts[0].path, 'leaflet-geosearch')
        self.assertEqual(scripts[0].file_name, 'geosearch.umd.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(styles[0].directory.endswith(np('/static/leaflet-geosearch')))
        self.assertEqual(styles[0].path, 'leaflet-geosearch')
        self.assertEqual(styles[0].file_name, 'geosearch.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

    def test_leaflet_markercluster_resources(self):
        resources_ = browser.leaflet_markercluster_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-markercluster')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-markercluster')
        self.assertEqual(resources_.path, 'leaflet-markercluster')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-markercluster')))
        self.assertEqual(scripts[0].path, 'leaflet-markercluster')
        self.assertEqual(scripts[0].file_name, 'leaflet.markercluster.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 2)

        self.assertTrue(styles[0].directory.endswith(np('/static/leaflet-markercluster')))
        self.assertEqual(styles[0].path, 'leaflet-markercluster')
        self.assertEqual(styles[0].file_name, 'MarkerCluster.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

        self.assertTrue(styles[1].directory.endswith(np('/static/leaflet-markercluster')))
        self.assertEqual(styles[1].path, 'leaflet-markercluster')
        self.assertEqual(styles[1].file_name, 'MarkerCluster.Default.css')
        self.assertTrue(os.path.exists(styles[1].file_path))

    def test_leaflet_editable_resources(self):
        resources_ = browser.leaflet_editable_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-editable')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-editable')
        self.assertEqual(resources_.path, 'leaflet-editable')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-editable')))
        self.assertEqual(scripts[0].path, 'leaflet-editable')
        self.assertEqual(scripts[0].file_name, 'Leaflet.Editable.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_leaflet_activearea_resources(self):
        resources_ = browser.leaflet_activearea_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-activearea')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-activearea')
        self.assertEqual(resources_.path, 'leaflet-activearea')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-activearea')))
        self.assertEqual(scripts[0].path, 'leaflet-activearea')
        self.assertEqual(scripts[0].file_name, 'leaflet.activearea.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_proj4_resources(self):
        resources_ = browser.proj4_resources
        self.assertTrue(resources_.directory.endswith(np('/static/proj4js')))
        self.assertEqual(resources_.name, 'cone.maps-proj4')
        self.assertEqual(resources_.path, 'proj4js')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/proj4js')))
        self.assertEqual(scripts[0].path, 'proj4js')
        self.assertEqual(scripts[0].file_name, 'proj4.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_leaflet_proj4_resources(self):
        resources_ = browser.leaflet_proj4_resources
        self.assertTrue(resources_.directory.endswith(np('/static/leaflet-proj4')))
        self.assertEqual(resources_.name, 'cone.maps-leaflet-proj4')
        self.assertEqual(resources_.path, 'leaflet-proj4')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/leaflet-proj4')))
        self.assertEqual(scripts[0].path, 'leaflet-proj4')
        self.assertEqual(scripts[0].file_name, 'proj4leaflet.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_cone_maps_resources(self):
        resources_ = browser.cone_maps_resources
        self.assertTrue(resources_.directory.endswith(np('/static/maps')))
        self.assertEqual(resources_.name, 'cone.maps-maps')
        self.assertEqual(resources_.path, 'maps')

        scripts = resources_.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/static/maps')))
        self.assertEqual(scripts[0].path, 'maps')
        self.assertEqual(scripts[0].file_name, 'cone.maps.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources_.styles
        self.assertEqual(len(styles), 0)

    def test_configure_resources(self):
        class TestConfigurator:
            def __init__(self):
                self.includes = {}

            def register_resource(self, resource):
                pass

            def set_resource_include(self, name, value):
                self.includes[name] = value

        configure_resources = browser.configure_resources
        config = TestConfigurator()
        settings = {
            'cone.maps.public': 'false'
        }
        configure_resources(config, settings)
        self.assertEqual(config.includes, {
            'leaflet-js': 'authenticated',
            'leaflet-css': 'authenticated',
            'leaflet-editable-js': False,
            'leaflet-pathdrag-js': False,
            'leaflet-nogap-js': False,
            'leaflet-geosearch-js': False,
            'leaflet-geosearch-css': False,
            'leaflet-markercluster-js': False,
            'leaflet-markercluster-css': False,
            'leaflet-markercluster-default-css': False,
            'leaflet-activearea-js': False,
            'proj4-js': False,
            'leaflet-proj4-js': False,
            'cone-maps-js': 'authenticated'
        })

        config = TestConfigurator()
        settings = {
            'cone.maps.public': 'false',
            'cone.maps.nogap': 'true',
            'cone.maps.geosearch': 'true',
            'cone.maps.markercluster': 'true',
            'cone.maps.editable': 'true',
            'cone.maps.pathdrag': 'true',
            'cone.maps.activearea': 'true',
            'cone.maps.proj4': 'true'
        }
        configure_resources(config, settings)
        self.assertEqual(config.includes, {
            'leaflet-js': 'authenticated',
            'leaflet-css': 'authenticated',
            'leaflet-editable-js': 'authenticated',
            'leaflet-pathdrag-js': 'authenticated',
            'leaflet-nogap-js': 'authenticated',
            'leaflet-geosearch-js': 'authenticated',
            'leaflet-geosearch-css': 'authenticated',
            'leaflet-markercluster-js': 'authenticated',
            'leaflet-markercluster-css': 'authenticated',
            'leaflet-markercluster-default-css': 'authenticated',
            'leaflet-activearea-js': 'authenticated',
            'proj4-js': 'authenticated',
            'leaflet-proj4-js': 'authenticated',
            'cone-maps-js': 'authenticated'
        })

        config = TestConfigurator()
        settings = {
            'cone.maps.public': 'true',
            'cone.maps.nogap': 'true',
            'cone.maps.geosearch': 'true',
            'cone.maps.markercluster': 'true',
            'cone.maps.editable': 'true',
            'cone.maps.pathdrag': 'true',
            'cone.maps.activearea': 'true',
            'cone.maps.proj4': 'true'
        }
        configure_resources(config, settings)
        self.assertEqual(config.includes, {
            'leaflet-js': True,
            'leaflet-css': True,
            'leaflet-editable-js': True,
            'leaflet-pathdrag-js': True,
            'leaflet-nogap-js': True,
            'leaflet-geosearch-js': True,
            'leaflet-geosearch-css': True,
            'leaflet-markercluster-js': True,
            'leaflet-markercluster-css': True,
            'leaflet-markercluster-default-css': True,
            'leaflet-activearea-js': True,
            'proj4-js': True,
            'leaflet-proj4-js': True,
            'cone-maps-js': True
        })
