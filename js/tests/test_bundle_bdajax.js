import $ from 'jquery';

// Separate test file, the bundle registers on DOM ready only once per page
QUnit.module('cone.maps.bundle.bdajax', (hooks) => {
    hooks.afterEach(() => {
        delete window.bdajax;
    });

    QUnit.test('bundle registers Map with bdajax if treibstoff is missing', async (assert) => {
        const registered = [];
        window.bdajax = {
            register: (func, instant) => {
                registered.push({ func, instant });
            },
        };

        const bundle = await import('../src/bundle.js');
        await new Promise((resolve) => $(resolve));

        assert.strictEqual(window.ts, undefined, 'treibstoff not present');
        assert.strictEqual(registered.length, 1, 'one registration');
        assert.strictEqual(registered[0].func, bundle.Map.initialize, 'initialize registered');
        assert.true(registered[0].instant, 'registered for instant execution');
    });
});
