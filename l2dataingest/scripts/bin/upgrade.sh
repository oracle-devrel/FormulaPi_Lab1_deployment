#!/bin/sh
F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)

# Reinstall if version is older than this (this creates changes in the setup that requires running the installation again)
REINSTALL_VERSION=16

cd $F1SIM_HOME

if [ -e "build.info" ]
then
    CP=`grep "GIT_REPO=" build.info | cut -d '=' -f 2`
    CT=`grep "TAG=" build.info | cut -d '=' -f 2`
    CV=`grep "BUILD_NUMBER=" build.info | cut -d '=' -f 2`
    CURRENT_BUILD="${CP}/${CP}-${CT}-${CV}.tar.gz"
else
    echo "Default to latest build."
    CV=0
fi

LATEST_BUILD=`curl https://apigw.withoracle.cloud/livelaps/rdm/packages/ | jq -rc --arg PROJECT "${CP}/${CP}" '[ .objects[] | select(.name | contains($PROJECT)) ] | last | .name'`

LV=`echo "${LATEST_BUILD}" | cut -d '.' -f 1 | rev | cut -d '-' -f 1 | rev`
LF=`echo "${LATEST_BUILD}" | cut -d '/' -f 2-`

if [ $((${CV} < ${LV})) = 0 ]
then
    echo "${CURRENT_BUILD} is the latest build."
    exit 1
fi

echo "${LATEST_BUILD} is the latest build. Installing."

echo "Downloading ${LATEST_BUILD}"
wget https://apigw.withoracle.cloud/livelaps/rdm/packages/${LATEST_BUILD}

echo "Extracting ${LATEST_BUILD}"
tar xzvf ${LF}

if [ $((${CV} < ${REINSTALL_VERSION})) ]
then
    echo "Required to reinstall. run the following command."
    echo ""
    echo "${F1SIM_HOME}/bin/install_pi.sh"
else
    echo "Required to restart. run the following command(s)."
    echo ""
    echo "sudo systemctl restart f1sim-webserver"
fi
