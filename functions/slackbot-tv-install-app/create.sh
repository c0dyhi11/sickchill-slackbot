#!/bin/bash
dir_name=${PWD##*/}
echo "Deploying Function $dir_name"
fission fn create --name $dir_name --code function.py --env python
echo "Deploying Route $dir_name"
fission route create --name $dir_name --function $dir_name --url /$dir_name
