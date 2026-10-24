import $ from 'jquery';
import * as map from '../src/map.js';
import cone_maps from '../src/maps.js';

QUnit.module('cone.maps.bundle', (hooks) => {
    hooks.afterEach(() => {
        delete window.ts;
    });

    QUnit.test('bundle exports Map and registers it with treibstoff', async (assert) => {
        const registered = [];
        window.ts = {
            ajax: {
                register: (func, instant) => {
                    registered.push({ func, instant });
                },
            },
        };

        const bundle = await import('../src/bundle.js');
        // ready callbacks run in registration order, this one after the bundle's
        await new Promise((resolve) => $(resolve));

        assert.deepEqual(Object.keys(bundle).sort(), ['Map', 'layer_factories'], 'exported names');
        assert.strictEqual(registered.length, 1, 'one registration');
        assert.strictEqual(registered[0].func, bundle.Map.initialize, 'initialize registered');
        assert.true(registered[0].instant, 'registered for instant execution');
    });
});

QUnit.module('cone.maps.maps', () => {
    QUnit.test('cone_maps namespace contains map API', (assert) => {
        assert.deepEqual(Object.keys(cone_maps).sort(), ['Map', 'layer_factories'], 'API names');
        assert.strictEqual(cone_maps.Map, map.Map, 'Map class');
        assert.strictEqual(cone_maps.layer_factories, map.layer_factories, 'layer factories');
    });
});
