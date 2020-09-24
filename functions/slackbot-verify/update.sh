#!/bin/bash
dir_name=${PWD##*/}
echo "Updating Function $dir_name"
fission fn update --name $dir_name --code function.py
