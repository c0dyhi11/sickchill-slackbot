#!/bin/bash
dir_name=${PWD##*/}
echo "Destroying Function $dir_name"
fission fn delete --name $dir_name
echo "Deleting all Packages built for Function $dir_name"
for i in `fission package list | grep "$dir_name" | awk '{print $1}'`; do
    fission package delete --name $i
done
