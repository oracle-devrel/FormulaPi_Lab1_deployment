#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)

cd $F1SIM_HOME

$F1SIM_HOME/bin/download_instantclient.sh -d $F1SIM_HOME -i $F1SIM_HOME -f
ORACLE_HOME=`ls .  -tp | grep instantclient_ | head -1 | xargs -I {} realpath {}`
$F1SIM_HOME/bin/download_rabbitmq.sh
$F1SIM_HOME/bin/setup_env.sh -d ${ORACLE_HOME} -f
$F1SIM_HOME/bin/setup_service.sh
WALLET_ZIPFILE=$(ls Wallet*.zip -tp | head -1)
if [ -z $WALLET_ZIPFILE ]
then 
    echo "Wallet ZIP file not found."
    echo "Upload the Wallet ZIP file in the $F1SIM_HOME directory and then run:"
    echo "$ bin/setup_wallet.sh -d $F1SIM_HOME -w <Wallet ZIP File> -f"
else
    $F1SIM_HOME/bin/setup_wallet.sh -d $F1SIM_HOME -w $WALLET_ZIPFILE -f
fi
$F1SIM_HOME/bin/setup_rabbitmq.sh
