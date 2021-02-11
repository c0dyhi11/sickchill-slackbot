#!/bin/bash
for i in `find . -mindepth 1 -type d -not -path '*/\.*'`; do
    cd $i
    ./update.sh
    cd ..
done
