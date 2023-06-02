#!/bin/sh

KERNEL=`uname -s`
MACHINE=`uname -m`
BASIC_URL=""
SQLPLUS_URL=""
DOWNLOAD_DIR=""
IC_DIR=""

print_usage()
{
    echo ""
    echo " download_instantclient.sh [-d DOWNLOAD_DIR] [-i IC_DIR] [-f] [-h]"
    echo ""
    echo " -d: where the Instant Client ZIP files are downloaded"
    echo " -i: where the Instant Client is unzipped (the instantclient_??_?? directory will be created in this directory)"
    echo " -f: force"
    echo " -h: this help"
    echo ""
}

while getopts 'd:i:fh' flag; do
  case "${flag}" in
    f) FORCE='true' ;;
    d) DOWNLOAD_DIR="${OPTARG}" ;;
    i) IC_DIR="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [ -z "$DOWNLOAD_DIR" ]
then
    read -p "Download Location: " DOWNLOAD_DIR
else
    echo "Download Location: ${DOWNLOAD_DIR}"
fi
if [ -z "$IC_DIR" ]
then
    read -p "Instant Client Location: " IC_DIR
fi

echo "Installing for $KERNEL $MACHINE"
if [ "$KERNEL" = "Linux" ]
then
    if [ "$MACHINE" = "aarch64" ]
    then
        BASIC_URL="https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basic-linux.arm64-19.10.0.0.0dbru.zip"
    elif [ "$MACHINE" = "x86_64" ]
    then
        BASIC_URL="https://download.oracle.com/otn_software/linux/instantclient/216000/instantclient-basic-linux.x64-21.6.0.0.0dbru.zip"
    else
        echo "$KERNEL $MACHINE not found"
        echo "Install Oracle Instant Client manually if supported by the platform"
        exit 1
    fi
else
    echo "$KERNEL $MACHINE not found"
    echo "Install Oracle Instant Client manually if supported by the platform"
    exit 1
fi 

BASIC_FILENAME=${BASIC_URL##*/}

echo "Downloading the following:"
echo "Basic Package: $BASIC_URL"

mkdir $DOWNLOAD_DIR
curl -o $DOWNLOAD_DIR/$BASIC_FILENAME $BASIC_URL

if [ "$FORCE" = "true" ]
then
    UNZIP_ARGS="-o"
fi
unzip -d $IC_DIR ${UNZIP_ARGS} $DOWNLOAD_DIR/$BASIC_FILENAME

echo "TODO: Update f1env.sh"
ORACLE_HOME=`ls .  -tp | grep instantclient_ | head -1 | xargs -I {} realpath {}`
echo "export ORACLE_HOME=$ORACLE_HOME"
