#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)

WALLET_DIRNAME=""

print_usage()
{
    echo ""
    echo " update_wallet.sh [-d WALLET_INSTALL_DIR] [-f] [-h]"
    echo ""
    echo " -d: where the Wallet is unzipped"
    echo " -f: force"
    echo " -h: help"
    echo ""
}

while getopts 'd:fh' flag; do
  case "${flag}" in
    f) FORCE='true' ;;
    d) WALLET_DIRNAME="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

. $F1SIM_HOME/f1env.sh

if [ "$ORACLE_HOME" = "" ]
then
    echo "ORACLE_HOME not set."
    echo "Run source ./f1env.sh"
    echo "Or setup environment bin/setup_env.sh"
    exit
fi

if [ -z "$WALLET_DIRNAME" ]
then
    read -p "Wallet Directory: " WALLET_DIRNAME
fi

WALLET_DIR=$(realpath $WALLET_DIRNAME)

if [ ! -e $WALLET_DIR/cwallet.sso ]
then
    echo "Wallet not found"
    exit
fi

cd $ORACLE_HOME/network/admin

if [ -L cwallet.sso ]
then
    echo "Wallet found."
    if [ "$FORCE" != "true" ]
    then
        while true
        do
            read -p "Continue (Y/N): " next
            case $next in
                [yY] )
                    break;;
                [nN] )
                    exit;;
                * ) echo invalid response;;
            esac
        done
    fi
fi

if [ -L cwallet.sso ]
then
    rm cwallet.sso
fi
ln -s $WALLET_DIR/cwallet.sso
if [ -L sqlnet.ora ]
then
    rm sqlnet.ora
fi
ln -s $WALLET_DIR/sqlnet.ora
if [ -L tnsnames.ora ]
then
    rm tnsnames.ora
fi
ln -s $WALLET_DIR/tnsnames.ora

echo "Wallet files linked to ${ORACLE_HOME}/network/admin"
echo "Current Status:"
ls -al ${ORACLE_HOME}/network/admin
