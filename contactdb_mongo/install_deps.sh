#!/bin/bash

set -e
set -x

BOOTSTRAP="3.0.2"

wget https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP}/bootstrap-${BOOTSTRAP}-dist.zip \
    -O bootstrap.zip

unzip -o -d contactdb/ bootstrap.zip
rsync contactdb/dist/* contactdb/static/
rm -rf contactdb/dist
rm bootstrap.zip
