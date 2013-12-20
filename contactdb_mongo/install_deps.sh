#!/bin/bash

set -e
set -x

BOOTSTRAP="3.0.3"

wget https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP}/bootstrap-${BOOTSTRAP}-dist.zip \
    -O bootstrap.zip

unzip -o -d contactdb/ bootstrap.zip
rsync -av contactdb/dist/* contactdb/static/
rm -rf contactdb/dist
rm bootstrap.zip

JQUERY="1.10.2"
wget http://code.jquery.com/jquery-${JQUERY}.min.js -O contactdb/static/js/jquery.js
