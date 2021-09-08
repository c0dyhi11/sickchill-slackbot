#!/bin/bash
dir_name=${PWD##*/}
echo "Copying helper functions"
cp ../helper.py package/
echo "Zipping up $dir_name"
zip -jr $dir_name.zip package/
echo "Creating $dir_name Package"
fission package create --name $dir_name --sourcearchive $dir_name.zip --env pythonsrc --buildcmd "./build.sh"
echo "Creating $dir_name Function"
fission fn create --name $dir_name --pkg $dir_name --entrypoint "function.main" --secret slackbot
echo "Creating $dir_name route"
fission route create --name $dir_name --function $dir_name --url $dir_name --method POST
echo "Deleting $dir_name.zip"
rm -f $dir_name.zip
echo "Deleting Helper Functions"
rm -f ./package/helper.py
