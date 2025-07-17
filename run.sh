#!/usr/bin/env bash
# fuck python envs...
export PATH=$(/usr/bin/realpath $(sed -e "s/run.sh$//" <(echo "$0")))
cd $PATH
source ./env/bin/activate
./main.py
deactivate
