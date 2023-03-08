#!/bin/sh

print_usage()
{
    echo ""
    echo " download_package.sh [-d INSTALL_HOME] [-u PACKAGE_BASEURL] [-p PACKAGE_NAME] [-h]"
    echo ""
    echo " -d: Wallet Install Directory"
    echo " -p: specific package to download"
    echo " -u: BASE URL where package is downloaded from"
    echo " -h: this help"
    echo ""
}

# Check existing installation version
INSTALL_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
if [ -e "${INSTALL_HOME}/build.info" ]
then
    cd ${INSTALL_HOME}
    CP=`grep "GIT_REPO=" build.info | cut -d '=' -f 2`
    CT=`grep "TAG=" build.info | cut -d '=' -f 2`
    CV=`grep "BUILD_NUMBER=" build.info | cut -d '=' -f 2`
    CURRENT_BUILD="${CP}/${CP}-${CT}-${CV}.tar.gz"
else
    CP="f1-simulator-cloud"
    echo "Default to latest build (and name)."
    CV=0
    INSTALL_HOME=""
fi

while getopts 'd:p:u:h' flag; do
    case "${flag}" in
    d) INSTALL_HOME="$(realpath ${OPTARG})" ;;
    p) PACKAGE_NAME="${OPTARG}" ;;
    u) PACKAGE_BASEURL="${OPTARG}" ;;
    *) print_usage
        exit 1 ;;
    esac
done
if [ -z "$INSTALL_HOME" ]
then
    read -p "Install Directory: " INSTALL_HOME
    INSTALL_HOME="$(realpath ${INSTALL_HOME})"
fi

# Download package
if [ -z "${PACKAGE_NAME}" ]
then 
    LATEST_BUILD=`curl -s ${PACKAGE_BASEURL} | jq -rc --arg PROJECT "${CP}/${CP}" '[ .objects[] | select(.name | contains($PROJECT)) ] | last | .name'`
else
    LATEST_BUILD="${PACKAGE_NAME}"
fi
echo ${LATEST_BUILD}

LV=`echo "${LATEST_BUILD}" | cut -d '.' -f 1 | rev | cut -d '-' -f 1 | rev`
LF=`echo "${LATEST_BUILD}" | cut -d '/' -f 2-`

if [ $((${CV} < ${LV})) = 0 ]
then
    echo "${CURRENT_BUILD} is the latest build."
    exit
fi

echo "${LATEST_BUILD} is the latest build. Installing."

if [ ! -d ${INSTALL_HOME}/dist ]
then
    mkdir ${INSTALL_HOME}/dist
fi

wget -O ${INSTALL_HOME}/dist/${LF} ${PACKAGE_BASEURL}${LATEST_BUILD}

# Unzip package
tar xzvf ${INSTALL_HOME}/dist/${LF} --directory=$INSTALL_HOME

if [ ! -d ${INSTALL_HOME}/log ]
then
    mkdir ${INSTALL_HOME}/log
fi

# temporary bug fix (to allow for previous incomplete apply)
# issue related to unzip of the package configuration doesn't overwrite / allow for existing configuration
# action is to remove SQL files that are unzipped
if [ -e "${INSTALL_HOME}/application/*.sql" ]
then
    rm ${INSTALL_HOME}/application/*.sql
fi
