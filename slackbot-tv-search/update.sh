#!/bin/bash
dir_name=${PWD##*/}
echo "Zipping up $dir_name"
zip -jr $dir_name.zip package/
echo "Updating $dir_name Package"
fission package update --name $dir_name --sourcearchive $dir_name.zip --env pythonsrc --buildcmd "./build.sh"
echo "Updating $dir_name Function"
fission fn update --name $dir_name --pkg $dir_name --entrypoint "function.main" --secret slackbot
echo "Deleting $dir_name.zip"
rm -f $dir_name.zip
