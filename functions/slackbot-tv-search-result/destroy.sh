#!/bin/bash
dir_name=${PWD##*/}
echo "Destroying Function $dir_name"
fission fn delete --name $dir_name
echo "Destroying MQTrigger $dir_name"
fission mqtrigger delete --name $dir_name
echo "Destroying Packages $dir_name"
fission package delete --name $dir_name

