import $ from 'jquery';

import {Map} from './map.js';

export * from './map.js';

$(function() {
    if (window.ts !== undefined) {
        ts.ajax.register(Map.initialize, true);
    } else {
        bdajax.register(Map.initialize, true);
    }
});
