#!/bin/sh

while getopts 'd:h' flag; do
    case "${flag}" in
    d) INSTALL_HOME="$(realpath ${OPTARG})" ;;
    *) print_usage
        exit 1 ;;
    esac
done

set -xe

UNAME_KERNEL=`uname -s`
UNAME_MACHINE=`uname -m`

if [ "${UNAME_KERNEL}" = "Linux" ]
then
    if [ "${UNAME_MACHINE}" = "x86_64" ]
    then
        DOWNLOAD_PLATFORM="linux-x64"
    elif [ "${UNAME_MACHINE}" = "arm64" ]
    then
        DOWNLOAD_PLATFORM="linux-aarch64"
    fi
elif [ "${UNAME_KERNEL}" = "Darwin" ]
then
    if [ "${UNAME_MACHINE}" = "x86_64" ]
    then
        DOWNLOAD_PLATFORM="macos-x64"
    elif [ "${UNAME_MACHINE}" = "arm64" ]
    then
        DOWNLOAD_PLATFORM="macos-aarch64"
    fi
fi

if [ "${DOWNLOAD_PLATFORM}" != "" ]
then
    if [ ! -d $(realpath ${INSTALL_HOME})/dist ]
    then
        mkdir $(realpath ${INSTALL_HOME})/dist
    fi
    wget -O $(realpath ${INSTALL_HOME})/dist/openjdk-11.0.2_${DOWNLOAD_PLATFORM}_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_${DOWNLOAD_PLATFORM}_bin.tar.gz
    tar xzvf $(realpath ${INSTALL_HOME})/dist/openjdk-11.0.2_${DOWNLOAD_PLATFORM}_bin.tar.gz --directory=$(realpath ${INSTALL_HOME})
else
    echo "Invalid OS version. Not supported."
    exit 255
fi
