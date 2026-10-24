import $ from 'jquery';

import { Map as ConeMap } from './map.js';

export * from './map.js';

$(() => {
    if (window.ts !== undefined) {
        ts.ajax.register(ConeMap.initialize, true);
    } else {
        bdajax.register(ConeMap.initialize, true);
    }
});
