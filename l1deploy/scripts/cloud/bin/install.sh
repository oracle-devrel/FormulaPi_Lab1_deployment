#!/bin/sh
INSTALL_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $INSTALL_HOME

TNS_ADMIN=""
TNS_PROFILE=""
DB_USER=""
DB_PASSWORD=""
DB_SCHEMA=""
APEX_WORKSPACE=""
ADMIN_PASSWORD=""
WALLET_INSTALL_DIR=""
WALLET_ZIPFILE=""

print_usage()
{
    echo ""
    echo " install.sh [-d WALLET_DIR] [-z WALLET_ZIPFILE] [-t TNS_PROFILE] [-u DB_USER] [-p DB_PASSWORD] [-s DB_SCHEMA] [-w APEX_WORKSPACE] [-a ADMIN_PASSWORD] [-h]"
    echo ""
    echo " -d: Wallet Install Directory"
    echo " -z: Wallet ZIP File"
    echo " -t: TNS profile used to connect to database"
    echo " -u: Database User (to create)"
    echo " -p: Database Password (to create for Database User)"
    echo " -s: Database Schema (for Database User)"
    echo " -w: APEX Workspace (to install APEX applications)"
    echo " -a: ADMIN Password"
    echo " -h: this help"
    echo ""
}

while getopts 'd:z:t:u:p:s:w:a:h' flag; do
  case "${flag}" in
    d) WALLET_INSTALL_DIR="$(realpath ${OPTARG})" ;;
    z) WALLET_ZIPFILE="$(realpath ${OPTARG})" ;;
    t) TNS_PROFILE="${OPTARG}" ;;
    u) DB_USER="${OPTARG}" ;;
    p) DB_PASSWORD="${OPTARG}" ;;
    s) DB_SCHEMA="${OPTARG}" ;;
    w) APEX_WORKSPACE="${OPTARG}" ;;
    a) ADMIN_PASSWORD="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [ "$ADMIN_PASSWORD" = "" ]
then
    stty -echo
    printf "ADMIN Password: "
    read ADMIN_PASSWORD
    stty echo
    printf "\n"
fi
if [ -z "$WALLET_INSTALL_DIR" ]
then
    read -p "Wallet Install Directory: " WALLET_INSTALL_DIR
    WALLET_INSTALL_DIR="$(realpath ${WALLET_INSTALL_DIR})"
fi
if [ -z "$WALLET_ZIPFILE" ]
then
    read -p "Wallet ZIP File: " WALLET_ZIPFILE
    WALLET_ZIPFILE="$(realpath ${WALLET_ZIPFILE})"
fi
if [ -z "$TNS_PROFILE" ]
then
    read -p "TNS Profile: " TNS_PROFILE
fi
if [ -z "$DB_USER" ]
then
    read -p "Database User: " DB_USER
fi
if [ "$DB_PASSWORD" = "" ]
then
    stty -echo
    printf "Database Password: "
    read DB_PASSWORD
    stty echo
    printf "\n"
fi
if [ -z "$DB_SCHEMA" ]
then
    read -p "Database Schema: " DB_SCHEMA
fi
if [ -z "$APEX_WORKSPACE" ]
then
    read -p "APEX Workspace: " APEX_WORKSPACE
fi

bin/download_sqlcl.sh

bin/setup_wallet.sh -z $(realpath ${WALLET_ZIPFILE}) -d ${WALLET_INSTALL_DIR}
WALLET_DIRNAME=$WALLET_INSTALL_DIR/$(realpath $WALLET_ZIPFILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)
WALLET_DIR=$(realpath $WALLET_DIRNAME)

if [ ! -d "./log" ] 
then
    mkdir log
fi

bin/create_user.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -s ${DB_SCHEMA} -w ${APEX_WORKSPACE} -a ${ADMIN_PASSWORD}

# APEX_ALIAS_INDEX=1
# for ii in `ls application/`
# do
#     APEX_FILE=`echo $ii | cut -d '.' -f 1 | cut -d 'f' -f 2` 
#     bin/deploy_apex.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -a "${ADMIN_PASSWORD}" -s ${DB_SCHEMA} -w ${APEX_WORKSPACE} -f ${APEX_FILE} -u change_me${APEX_ALIAS_INDEX}
#     let APEX_ALIAS_INDEX=${APEX_ALIAS_INDEX}+1
# done

bin/deploy_model.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f controller.xml

# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1max-session
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1max-lapdata
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1max-laptime
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1max-motion
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1max-telemetry
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1sim-track
# bin/deploy_data.sh -t ${TNS_PROFILE} -d ${WALLET_DIR} -u ${DB_USER} -p "${DB_PASSWORD}" -f f1sim-trackdata
