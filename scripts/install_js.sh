#!/bin/bash

set -e

if ! which npm &> /dev/null; then
    sudo apt-get install npm
fi

npm --prefix . --save-dev install \
    qunit \
    karma \
    karma-qunit \
    karma-coverage \
    karma-chrome-launcher \
    karma-module-resolver-preprocessor \
    rollup \
    rollup-plugin-cleanup \
    rollup-plugin-terser \

npm --prefix . --no-save install \
    https://github.com/jquery/jquery#main
