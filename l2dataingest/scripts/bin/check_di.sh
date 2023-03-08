#!/bin/sh
F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $F1SIM_HOME

# print status and output of the consumer
sudo systemctl status --no-pager -l f1sim-consumer
# print status and output of the producer
sudo systemctl status --no-pager -l f1sim-producer
# print status of which wallet is being used or referenced
# if no output is shown then instantclient is not installed
# if no export ORACLE_HOME is shown then the instantclient found is not configured in the f1env.sh
# if no files are shown (ie empty directory) then the wallet is not installed
find $F1SIM_HOME -wholename /*instantclient_??_?? | xargs -i sh -c 'cat f1env.sh | grep {}; ls -al {}/network/admin'
# print output the common configuration from the f1store
grep 'gamehost:' f1store.yaml
grep 'devicename:' f1store.yaml
grep 'store:' f1store.yaml
grep 'forward:' f1store.yaml
grep 'dburl:' f1store.yaml
grep 'dbusername:' f1store.yaml
grep 'dbpassword:' f1store.yaml
grep 'poolsize:' f1store.yaml
