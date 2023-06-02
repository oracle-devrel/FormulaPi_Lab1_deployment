#!/bin/sh
F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $F1SIM_HOME

. dev/bin/activate
. ./f1env.sh

export FLASK_APP="$F1SIM_HOME/web/f1sim-dash.py"
#export FLASK_ENV=development
#nohup sudo -E flask run --host=0.0.0.0 --port=80 > /dev/null 2>&1 &
flask run --host=0.0.0.0 --port=8080
