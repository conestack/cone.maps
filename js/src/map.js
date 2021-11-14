import $ from 'jquery';

export function lookup_factory(name) {
    let ob = window;
    for (let part of name.split('.')) {
        ob = ob[part];
        if (ob === undefined) {
            throw "Cannot locate map factory: " + name;
        }
    }
    return ob;
}

let layer_factories = {};
export {layer_factories};

layer_factories.tile_layer = function(inst, cfg) {
    inst.layer_created(new L.tileLayer(cfg.urlTemplate, cfg.options), cfg);
}

layer_factories.geo_json = function(inst, cfg) {
    $.getJSON(cfg.dataUrl, function(data) {
        inst.layer_created(new L.geoJSON(data, cfg.options), cfg);
    });
}

export class Map {

    static initialize(context) {
        $('div.cone_map', context).each(function() {
            let elem = $(this);
            let factory = lookup_factory(elem.data('map-factory'));
            new factory(elem);
        });
    }

    constructor(elem) {
        this.elem = elem;
        this.id = elem.attr('id');
        this.layers = elem.data('map-layers');
        this.default_center = elem.data('map-center');
        this.default_zoom = elem.data('map-zoom');
        this.map_options = elem.data('map-options');
        this.control_options = elem.data('map-control-options');
        this.source = elem.data('map-source');
        this.create();
        elem.data('map-instance', this);
    }

    create() {
        this.create_map();
        this.create_controls();
        this.create_layers();
    }

    create_map() {
        this.map = L.map(this.id, this.map_options);
        this.map.setView(this.default_center, this.default_zoom);
    }

    create_controls() {
        let base_maps = [],
            overlay_maps = [];
        this.map_layers = new L.control.layers(
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
}
