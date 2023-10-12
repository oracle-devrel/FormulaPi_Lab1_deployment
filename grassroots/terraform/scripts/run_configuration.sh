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

scripts/download_package.sh -d $(realpath ${INSTALL_HOME}) -u ${PACKAGE_BASEURL} ${PACKAGE_OPTIONS}
$(realpath ${INSTALL_HOME})/bin/install.sh -d $(realpath ${INSTALL_HOME}) -z $(realpath ${WALLET_DIR})/wallet.zip -t ${ADB_NAME}_low -u ${DB_USER} -s ${DB_SCHEMA} -w ${APEX_WORKSPACE} -p ${DB_PASSWORD} -a ${ADMIN_PASSWORD}
