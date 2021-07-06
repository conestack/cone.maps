if (window.cone === undefined) {
    cone = {};
}

(function($) {

    let maps = cone.maps = {};

    maps.lookup_factory = function(name) {
        let ob = window;
        for (let part of name.split('.')) {
            ob = ob[part];
            if (ob === undefined) {
                throw "Cannot locate map factory: " + name;
            }
        }
        return ob;
    };

    let layer_factories = maps.layer_factories = {};

    layer_factories.tile_layer = function(cfg, map) {
        new L.tileLayer(cfg.urlTemplate, cfg.options).addTo(map);
    };

    layer_factories.geo_json = function(cfg, map) {
        $.getJSON(cfg.dataUrl, function(data) {
            new L.geoJSON(data, cfg.options).addTo(map);
        });
    };

    maps.Map = class {

        static initialize(context) {
            $('div.cone_map', context).each(function() {
                let elem = $(this);
                let factory = maps.lookup_factory(elem.data('map-factory'));
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
            this.source = elem.data('map-source');

            this.create();

            elem.data('map-instance', this);
        }

        create() {
            this.create_map();
            this.create_layers();
            this.create_controls();
        }

        create_map() {
            this.map = L.map(this.id, this.map_options);
            this.map.setView(this.default_center, this.default_zoom);
        }

        create_layers() {
            for (let l of this.layers) {
                layer_factories[l.factory](l, this.map);
            }
        }

        create_controls() {
        }
    }

    $(document).ready(function() {
        bdajax.register(function(context) {
            maps.Map.initialize(context);
        }, true);
    });

})(jQuery);
