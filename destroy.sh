#!/bin/bash
for i in *; do
    if [ "$i" != "create.sh" ] && [ "$i" != "update.sh" ] && [ "$i" != "destroy.sh" ]; then
        cd $i
        ./destroy.sh
        cd ..
    fi
done
fission env delete --name pythonsrc
fission env delete --name python
