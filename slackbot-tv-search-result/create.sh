#!/bin/bash
dir_name=${PWD##*/}
echo "Creating $dir_name Function"
fission fn create --name $dir_name --code function.py --env python --secret slackbot
echo "Creating $dir_name MQTrigger"
fission mqtrigger create --name $dir_name --function $dir_name --topic tv-request
