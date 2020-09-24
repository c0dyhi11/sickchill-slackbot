#!/bin/bash
fission env create --name pythonsrc --image fission/python-env:latest --builder fission/python-builder:latest
fission env create --name python --image fission/python-env
for i in `find . -mindepth 1 -type d -not -path '*/\.*'`; do
    cd $i
    ./create.sh
    cd ..
done
