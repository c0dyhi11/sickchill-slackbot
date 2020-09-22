#!/bin/bash
for i in *; do
    if [ "$i" != "create.sh" ] && [ "$i" != "update.sh" ] && [ "$i" != "destroy.sh" ]; then
        cd $i
        ./update.sh
        cd ..
    fi
done
