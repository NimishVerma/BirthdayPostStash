#!/bin/bash

ABS_ENV_DIR=$(cd ${1:-~/env/bpstash/} && pwd -P)
source $ABS_ENV_DIR/bin/activate

ABS_WORK_DIR=`pwd -P`
# LOCAL_PYTHONPATH=${ABS_WORK_DIR}/apps:${ABS_WORK_DIR}/lib:${ABS_WORK_DIR}/local
export PYTHONPATH=$LOCAL_PYTHONPATH

export DJANGO_SETTINGS_MODULE=${2:-BirthdayPostStash}.settings

echo "Using virtualenv from $ABS_ENV_DIR"
echo "Set PYTHONPATH to $PYTHONPATH"
echo "Set DJANGO_SETTINGS_MODULE to $DJANGO_SETTINGS_MODULE"
