import $ from 'jquery';

import {Map} from './map.js';

export * from './map.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(maps.Map.initialize, true);
    } else {
        bdajax.register(maps.Map.initialize, true);
    }
});
