#!/bin/sh
INSTALL_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $INSTALL_HOME

if [ ! -d sqlcl ]
then
    # Download
    if [ ! -d dist ]
    then
        mkdir dist
    fi

    curl -o dist/sqlcl-latest.zip https://download.oracle.com/otn_software/java/sqldeveloper/sqlcl-latest.zip

    # Unzip sqlcl
    unzip dist/sqlcl-latest.zip
fi
