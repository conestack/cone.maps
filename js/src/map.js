import $ from 'jquery';

let layer_factories = {};
export {layer_factories};

layer_factories.tile_layer = function(inst, cfg) {
    inst.layer_created(new L.TileLayer(cfg.urlTemplate, cfg.options), cfg);
}

layer_factories.geo_json = function(inst, cfg) {
    $.getJSON(cfg.dataUrl, function(data) {
        inst.layer_created(new L.GeoJSON(data, cfg.options), cfg);
    });
}

export class Map {

    static initialize(context) {
        $('div.cone-map', context).each(function() {
            let elem = $(this),
                settings = elem.data('map-settings'),
                factory_path = settings.factory,
                factory = ts.object_by_path(factory_path);
            new factory(elem, settings);
        });
    }

    constructor(elem, settings) {
        this.elem = elem;
        this.id = elem.attr('id');

        this.layers = settings.layers
        this.default_center = settings.center
        this.default_zoom = settings.zoom
        this.default_bounds = settings.bounds
        this.map_options = settings.options
        this.control_options = settings.control_options
        this.markers = settings.markers
        this.markers_source = settings.markers_source
        this.marker_groups = settings.groups
        this.marker_groups_source = settings.groups_source

        this.create();
        elem.data('map-instance', this);
    }

    create() {
        this.create_map();
        this.create_controls();
        this.create_layers();
        this.create_markers();
    }

    create_map() {
        this.map = new L.Map(this.id, this.map_options);
        if (this.default_bounds.length) {
            this.map.fitBounds(this.default_bounds);
        } else {
            this.map.setView(this.default_center, this.default_zoom);
        }
    }

    create_controls() {
        let base_maps = [],
            overlay_maps = [];
        this.map_layers = new L.Control.Layers(
            base_maps,
            overlay_maps,
            this.control_options
        );
        this.map_layers.addTo(this.map);
    }

    create_layers() {
        for (let l of this.layers) {
            layer_factories[l.factory](this, l);
        }
    }

    layer_created(layer, cfg) {
        cfg.layer = layer;
        if (cfg.display === undefined || cfg.display) {
            this.add_layer(layer);
        }
        if (cfg.category === 'base') {
            this.map_layers.addBaseLayer(layer, cfg.title);
        } else if (cfg.category === 'overlay') {
            this.map_layers.addOverlay(layer, cfg.title);
        }
    }

    add_layer(layer) {
        this.map.addLayer(layer);
    }

    remove_layer(layer) {
        this.map.removeLayer(layer);
    }

    create_markers() {
        for (let marker of this.markers) {
            this.create_marker(marker);
        }
        if (this.markers_source) {
            $.getJSON(this.markers_source, function(data) {
                for (let marker of data) {
                    this.create_marker(marker);
                }
            }.bind(this));
        }
        if (this.markers || this.markers_source) {
            this.map.on('popupopen', function(evt) {
                let popup = evt.popup;
                ts.ajax.bind($(popup._contentNode));
            });
        }
    }

    create_marker(marker) {
        let m = new L.Marker(marker.latlng, marker.options).addTo(this.map);
        if (marker.popup) {
            m.bindPopup(marker.popup.content, marker.popup.options);
        }
    }
}
