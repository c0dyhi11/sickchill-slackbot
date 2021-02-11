#!/bin/bash
dir_name=${PWD##*/}
echo "Creating $dir_name Function"
fission fn create --name $dir_name --code function.py --env python
