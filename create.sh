#!/bin/bash
fission env create --name pythonsrc --image fission/python-env:latest --builder fission/python-builder:latest
fission env create --name python --image fission/python-env
for i in *; do
    if [ "$i" != "create.sh" ] && [ "$i" != "update.sh" ] && [ "$i" != "destroy.sh" ]; then
        cd $i
        ./create.sh
        cd ..
    fi
done
