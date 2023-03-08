#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)

WALLET_ZIPFILE=""
WALLET_INSTALL_DIR=""

print_usage()
{
    echo ""
    echo " setup_wallet.sh [-d WALLET_INSTALL_DIR] [-w WALLET_ZIPFILE] [-f] [-h]"
    echo ""
    echo " -w: Wallet ZIP file to install"
    echo " -d: where the Wallet is unzipped"
    echo " -f: force"
    echo " -h: this help"
    echo ""
}

while getopts 'd:w:fh' flag; do
  case "${flag}" in
    f) FORCE='true' ;;
    d) WALLET_INSTALL_DIR="${OPTARG}" ;;
    w) WALLET_ZIPFILE="${OPTARG}" ;;
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

if [ -z "$WALLET_ZIPFILE" ] 
then
    read -p "Wallet (ZIP) File: " WALLET_ZIPFILE
fi
if [ -z "$WALLET_INSTALL_DIR" ] 
then
    read -p "Wallet Install Directory: " WALLET_INSTALL_DIR
fi

WALLET_DIRNAME=$WALLET_INSTALL_DIR/$(realpath $WALLET_ZIPFILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)
mkdir -p $WALLET_DIRNAME
WALLET_DIR=$(realpath $WALLET_DIRNAME)

if [ "$FORCE" = "true" ]
then
    UNZIP_ARGS="-o"
fi
unzip -d $WALLET_DIRNAME ${UNZIP_ARGS} $WALLET_ZIPFILE

echo "Wallet unzipped into ${WALLET_DIR}"

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
