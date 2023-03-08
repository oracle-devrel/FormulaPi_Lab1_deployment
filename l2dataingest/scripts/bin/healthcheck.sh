#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $F1SIM_HOME

. dev/bin/activate
. ./f1env.sh
python3 src/healthcheck.py
