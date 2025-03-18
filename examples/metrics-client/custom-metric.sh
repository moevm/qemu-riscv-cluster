#!/bin/bash
set -e

x=$(date '+%s')
y=$(echo ${x} | awk "{print sin(\$1 / 100)}")
echo "{ \"fields\": { \"field_1\": ${y} }, \"timestamp\": ${x} }"
