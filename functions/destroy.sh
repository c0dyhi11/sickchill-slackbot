#!/bin/bash
for i in `find . -mindepth 1 -type d -not -path '*/\.*'`; do
    cd $i
    ./destroy.sh
    cd ..
done
fission env delete --name pythonsrc
fission env delete --name python
