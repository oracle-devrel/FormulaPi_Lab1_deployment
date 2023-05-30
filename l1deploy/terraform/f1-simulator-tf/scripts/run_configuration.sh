#!/usr/bin/env bash

if [ ! -d $(realpath ${INSTALL_HOME})/dist ]
then
    mkdir $(realpath ${INSTALL_HOME})/dist
fi

if [ "${PACKAGE_NAME}" != "" ]
then
    PACKAGE_OPTION="-p ${PACKAGE_NAME}"
else
    PACKAGE_OPTION=""
fi

JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d '"' -f 2  | cut -d '.' -f 1)

if [ $JAVA_VERSION -lt 11 ]
then
    VERSION="20.0.1"
    scripts/install_jdk.sh -d ${INSTALL_HOME} -v ${VERSION}
    export JAVA_HOME=$(realpath ${INSTALL_HOME})/jdk-${VERSION}
    export PATH=${JAVA_HOME}/bin:${PATH}
    echo ${PATH}
fi

scripts/download_package.sh -d $(realpath ${INSTALL_HOME}) -u ${PACKAGE_BASEURL} ${PACKAGE_OPTIONS}
$(realpath ${INSTALL_HOME})/bin/install.sh -z $(realpath ${WALLET_DIR})/wallet.zip -t ${ADB_NAME}_low -u ${DB_USER} -s ${DB_SCHEMA} -w ${APEX_WORKSPACE} -p ${DB_PASSWORD} -d $(realpath ${INSTALL_HOME})/dist -a ${ADMIN_PASSWORD}
