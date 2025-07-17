#!/usr/bin/env bash
# fuck python envs...
cd $(realpath $(dirname $0))
source ./env/bin/activate
./main.py
deactivate
