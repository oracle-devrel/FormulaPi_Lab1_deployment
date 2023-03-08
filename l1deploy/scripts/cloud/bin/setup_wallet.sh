#!/bin/sh
INSTALL_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $INSTALL_HOME

WALLET_ZIPFILE=""
WALLET_INSTALL_DIR=""

print_usage()
{
    echo ""
    echo " setup_wallet.sh [-d WALLET_INSTALL_DIR] [-z WALLET_ZIPFILE] [-h]"
    echo ""
    echo " -z: Wallet ZIP file to install"
    echo " -d: where the Wallet is unzipped"
    echo " -h: this help"
    echo ""
}

while getopts 'z:d:h' flag; do
  case "${flag}" in
    d) WALLET_INSTALL_DIR="$(realpath ${OPTARG})" ;;
    z) WALLET_ZIPFILE="$(realpath ${OPTARG})" ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [ -z "$WALLET_ZIPFILE" ]
then
    read -p "Wallet (ZIP) File: " WALLET_ZIPFILE
    WALLET_INSTALL_DIR="$(realpath ${WALLET_ZIPFILE})"
fi
if [ -z "$WALLET_INSTALL_DIR" ]
then
    read -p "Wallet Install Directory: " WALLET_INSTALL_DIR
    WALLET_ZIPFILE="$(realpath ${WALLET_INSTALL_DIR})"
fi

WALLET_DIRNAME=$WALLET_INSTALL_DIR/$(realpath $WALLET_ZIPFILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)
mkdir -p $WALLET_DIRNAME
WALLET_DIR=$(realpath $WALLET_DIRNAME)

unzip -o -d $WALLET_DIRNAME $(realpath $WALLET_ZIPFILE)

# Configure sqlnet.ora
# sed -i "s#?/network/admin#$WALLET_DIRNAME#" $WALLET_DIRNAME/sqlnet.ora
echo "WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY=${WALLET_DIR})))
SSL_SERVER_DN_MATCH=yes" > "${WALLET_DIR}/sqlnet.ora"

export TNS_ADMIN="${WALLET_DIR}"
