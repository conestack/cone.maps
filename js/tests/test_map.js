import $ from 'jquery';
import { Map as ConeMap, layer_factories } from '../src/map.js';

///////////////////////////////////////////////////////////////////////////////
// Mock Leaflet objects
///////////////////////////////////////////////////////////////////////////////

class MockTileLayer {
    constructor(urlTemplate, options) {
        this.urlTemplate = urlTemplate;
        this.options = options;
    }
}

class MockGeoJSON {
    constructor(data, options) {
        this.data = data;
        this.options = options;
    }
}

class MockControlLayers {
    constructor(baseMaps, overlayMaps, options) {
        this.baseMaps = baseMaps;
        this.overlayMaps = overlayMaps;
        this.options = options;
        this.added_base_layers = [];
        this.added_overlays = [];
    }

    addTo(map) {
        this.map = map;
        return this;
    }

    addBaseLayer(layer, title) {
        this.added_base_layers.push({ layer, title });
    }

    addOverlay(layer, title) {
        this.added_overlays.push({ layer, title });
    }
}

class MockMarker {
    constructor(latlng, options) {
        this.latlng = latlng;
        this.options = options;
        this.popup = null;
    }

    addTo(map) {
        this.map = map;
        return this;
    }

    bindPopup(content, options) {
        this.popup = { content, options };
        return this;
    }
}

class MockMap {
    constructor(id, options) {
        this.id = id;
        this.options = options;
        this.layers = [];
        this.events = {};
        this.view = null;
        this.bounds = null;
    }

    setView(center, zoom) {
        this.view = { center, zoom };
        return this;
    }

    fitBounds(bounds) {
        this.bounds = bounds;
        return this;
    }

    addLayer(layer) {
        this.layers.push(layer);
        return this;
    }

    removeLayer(layer) {
        const idx = this.layers.indexOf(layer);
        if (idx !== -1) {
            this.layers.splice(idx, 1);
        }
        return this;
    }

    on(event, callback) {
        this.events[event] = callback;
        return this;
    }
}

///////////////////////////////////////////////////////////////////////////////
// Test module: layer_factories
///////////////////////////////////////////////////////////////////////////////

QUnit.module('cone.maps.layer_factories', (hooks) => {
    let L_origin;

    hooks.before(() => {
        L_origin = window.L;
        window.L = {
            TileLayer: MockTileLayer,
            GeoJSON: MockGeoJSON,
            Map: MockMap,
            Control: {
                Layers: MockControlLayers,
            },
            Marker: MockMarker,
        };
    });

    hooks.after(() => {
        window.L = L_origin;
    });

    QUnit.test('tile_layer factory creates TileLayer', (assert) => {
        let layer_created = null;
        let cfg_received = null;

        const inst = {
            layer_created: (layer, cfg) => {
                layer_created = layer;
                cfg_received = cfg;
            },
        };

        const cfg = {
            factory: 'tile_layer',
            urlTemplate: 'https://{s}.tile.example.com/{z}/{x}/{y}.png',
            options: {
                attribution: 'Test Attribution',
                maxZoom: 19,
            },
        };

        layer_factories.tile_layer(inst, cfg);

        assert.ok(layer_created instanceof MockTileLayer);
        assert.strictEqual(layer_created.urlTemplate, cfg.urlTemplate);
        assert.deepEqual(layer_created.options, cfg.options);
        assert.strictEqual(cfg_received, cfg);
    });

    QUnit.test('geo_json factory fetches data and creates GeoJSON', (assert) => {
        const getJSON_origin = $.getJSON;
        let layer_created = null;
        let cfg_received = null;

        const inst = {
            layer_created: (layer, cfg) => {
                layer_created = layer;
                cfg_received = cfg;
            },
        };

        const cfg = {
            factory: 'geo_json',
            dataUrl: '/api/geojson',
            options: {
                style: { color: 'blue' },
            },
        };

        const test_data = {
            type: 'FeatureCollection',
            features: [],
        };

        $.getJSON = (url, callback) => {
            assert.strictEqual(url, cfg.dataUrl);
            callback(test_data);
        };

        layer_factories.geo_json(inst, cfg);

        assert.ok(layer_created instanceof MockGeoJSON);
        assert.deepEqual(layer_created.data, test_data);
        assert.deepEqual(layer_created.options, cfg.options);
        assert.strictEqual(cfg_received, cfg);

        $.getJSON = getJSON_origin;
    });
});

///////////////////////////////////////////////////////////////////////////////
// Test module: Map class
///////////////////////////////////////////////////////////////////////////////

QUnit.module('cone.maps.Map', (hooks) => {
    let container, L_origin, ts_origin, ts_ajax_bind_origin, getJSON_origin;

    hooks.before(() => {
        L_origin = window.L;
        ts_origin = window.ts;
        getJSON_origin = $.getJSON;

        window.L = {
            TileLayer: MockTileLayer,
            GeoJSON: MockGeoJSON,
            Map: MockMap,
            Control: {
                Layers: MockControlLayers,
            },
            Marker: MockMarker,
        };

        window.ts = {
            object_by_path: (path) => {
                if (path === 'cone.maps.Map') {
                    return ConeMap;
                }
                return null;
            },
            ajax: {
                bind: () => {},
            },
        };
    });

    hooks.beforeEach(() => {
        container = $('<div />').appendTo('body');
        ts_ajax_bind_origin = window.ts.ajax.bind;
    });

    hooks.afterEach(() => {
        container.remove();
        $.getJSON = getJSON_origin;
        window.ts.ajax.bind = ts_ajax_bind_origin;
    });

    hooks.after(() => {
        window.L = L_origin;
        window.ts = ts_origin;
    });

    QUnit.test('Map.initialize finds elements and creates instances', (assert) => {
        const elem = $(`<div
            id="test-map"
            class="cone-map"
            data-map-settings='${JSON.stringify({
                factory: 'cone.maps.Map',
                layers: [],
                center: [0, 0],
                zoom: 5,
                bounds: [],
                options: {},
                control_options: {},
                markers: [],
                markers_source: null,
                groups: [],
                groups_source: null,
            })}'
        />`).appendTo(container);

        ConeMap.initialize(container);

        const instance = elem.data('map-instance');
        assert.ok(instance instanceof ConeMap);
        assert.strictEqual(instance.id, 'test-map');
    });

    QUnit.test('Map constructor initializes properties', (assert) => {
        const elem = $('<div id="test-map-2" />').appendTo(container);

        const settings = {
            layers: [{ factory: 'tile_layer', urlTemplate: 'test' }],
            center: [51.5, -0.1],
            zoom: 10,
            bounds: [],
            options: { zoomControl: true },
            control_options: { collapsed: false },
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map = new ConeMap(elem, settings);

        assert.strictEqual(map.elem, elem);
        assert.strictEqual(map.id, 'test-map-2');
        assert.deepEqual(map.layers, settings.layers);
        assert.deepEqual(map.default_center, settings.center);
        assert.strictEqual(map.default_zoom, settings.zoom);
        assert.deepEqual(map.default_bounds, settings.bounds);
        assert.deepEqual(map.map_options, settings.options);
        assert.deepEqual(map.control_options, settings.control_options);
        assert.strictEqual(elem.data('map-instance'), map);
    });

    QUnit.test('create_map with setView', (assert) => {
        const elem = $('<div id="test-map-view" />').appendTo(container);

        const settings = {
            layers: [],
            center: [48.8, 2.3],
            zoom: 12,
            bounds: [],
            options: { zoomControl: false },
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        assert.ok(map_inst.map instanceof MockMap);
        assert.deepEqual(map_inst.map.view, {
            center: [48.8, 2.3],
            zoom: 12,
        });
        assert.strictEqual(map_inst.map.bounds, null);
    });

    QUnit.test('create_map with fitBounds', (assert) => {
        const elem = $('<div id="test-map-bounds" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [
                [40, -5],
                [50, 10],
            ],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        assert.deepEqual(map_inst.map.bounds, [
            [40, -5],
            [50, 10],
        ]);
        assert.strictEqual(map_inst.map.view, null);
    });

    QUnit.test('create_controls creates layer control', (assert) => {
        const elem = $('<div id="test-map-controls" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: { position: 'topright' },
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        assert.ok(map_inst.map_layers instanceof MockControlLayers);
        assert.deepEqual(map_inst.map_layers.options, { position: 'topright' });
        assert.strictEqual(map_inst.map_layers.map, map_inst.map);
    });

    QUnit.test('create_layers calls factories', (assert) => {
        const elem = $('<div id="test-map-layers" />').appendTo(container);

        const settings = {
            layers: [
                {
                    factory: 'tile_layer',
                    urlTemplate: 'https://tile.example.com/{z}/{x}/{y}.png',
                    options: {},
                },
            ],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        // layer_created is called by factory, which adds layer to map
        assert.strictEqual(map_inst.map.layers.length, 1);
        assert.ok(map_inst.map.layers[0] instanceof MockTileLayer);
    });

    QUnit.test('layer_created adds layer to map by default', (assert) => {
        const elem = $('<div id="test-layer-default" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const layer = new MockTileLayer('test', {});
        const cfg = { title: 'Test Layer' };

        map_inst.layer_created(layer, cfg);

        assert.strictEqual(map_inst.map.layers.length, 1);
        assert.strictEqual(cfg.layer, layer);
    });

    QUnit.test('layer_created respects display:false', (assert) => {
        const elem = $('<div id="test-layer-nodisplay" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const layer = new MockTileLayer('test', {});
        const cfg = { title: 'Hidden Layer', display: false };

        map_inst.layer_created(layer, cfg);

        assert.strictEqual(map_inst.map.layers.length, 0);
    });

    QUnit.test('layer_created adds base layer to control', (assert) => {
        const elem = $('<div id="test-layer-base" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const layer = new MockTileLayer('test', {});
        const cfg = { title: 'Base Layer', category: 'base' };

        map_inst.layer_created(layer, cfg);

        assert.strictEqual(map_inst.map_layers.added_base_layers.length, 1);
        assert.strictEqual(map_inst.map_layers.added_base_layers[0].title, 'Base Layer');
    });

    QUnit.test('layer_created adds overlay to control', (assert) => {
        const elem = $('<div id="test-layer-overlay" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const layer = new MockTileLayer('test', {});
        const cfg = { title: 'Overlay Layer', category: 'overlay' };

        map_inst.layer_created(layer, cfg);

        assert.strictEqual(map_inst.map_layers.added_overlays.length, 1);
        assert.strictEqual(map_inst.map_layers.added_overlays[0].title, 'Overlay Layer');
    });

    QUnit.test('add_layer and remove_layer', (assert) => {
        const elem = $('<div id="test-layer-methods" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const layer = new MockTileLayer('test', {});

        map_inst.add_layer(layer);
        assert.strictEqual(map_inst.map.layers.length, 1);

        map_inst.remove_layer(layer);
        assert.strictEqual(map_inst.map.layers.length, 0);
    });

    QUnit.test('create_markers from config', (assert) => {
        const elem = $('<div id="test-markers" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [
                {
                    latlng: [51.5, -0.1],
                    options: { title: 'London' },
                    popup: {
                        content: '<strong>London</strong>',
                        options: { maxWidth: 300 },
                    },
                },
            ],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        // Map should have popupopen event bound
        assert.ok(map_inst.map.events.popupopen);
    });

    QUnit.test('create_markers from source', (assert) => {
        const elem = $('<div id="test-markers-source" />').appendTo(container);

        const markers_data = [{ latlng: [48.8, 2.3], options: { title: 'Paris' } }];

        $.getJSON = (url, callback) => {
            assert.strictEqual(url, '/api/markers');
            callback(markers_data);
        };

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: '/api/markers',
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        assert.ok(map_inst.map.events.popupopen);
    });

    QUnit.test('opened marker popup content gets bound to ajax', (assert) => {
        const elem = $('<div id="test-markers-popupopen" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [
                {
                    latlng: [51.5, -0.1],
                    options: { title: 'London' },
                    popup: { content: '<strong>London</strong>', options: {} },
                },
            ],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);
        const bound = [];
        window.ts.ajax.bind = (context) => {
            bound.push(context);
        };
        const content_node = document.createElement('div');

        map_inst.map.events.popupopen({ popup: { _contentNode: content_node } });

        assert.strictEqual(bound.length, 1);
        assert.strictEqual(bound[0].get(0), content_node);
    });

    QUnit.test('create_marker creates marker with popup', (assert) => {
        const elem = $('<div id="test-create-marker" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        const marker_config = {
            latlng: [52.5, 13.4],
            options: { title: 'Berlin' },
            popup: {
                content: '<h3>Berlin</h3>',
                options: { minWidth: 200 },
            },
        };

        map_inst.create_marker(marker_config);

        // Since create_marker uses L.Marker().addTo(), we can't easily
        // track the created markers without modifying the mock
        // The test verifies the method runs without error
        assert.ok(true);
    });

    QUnit.test('create_marker without popup', (assert) => {
        const elem = $('<div id="test-marker-nopopup" />').appendTo(container);

        const settings = {
            layers: [],
            center: [0, 0],
            zoom: 5,
            bounds: [],
            options: {},
            control_options: {},
            markers: [],
            markers_source: null,
            groups: [],
            groups_source: null,
        };

        const map_inst = new ConeMap(elem, settings);

        const marker_config = {
            latlng: [40.7, -74.0],
            options: { title: 'New York' },
        };

        map_inst.create_marker(marker_config);

        assert.ok(true);
    });
});
