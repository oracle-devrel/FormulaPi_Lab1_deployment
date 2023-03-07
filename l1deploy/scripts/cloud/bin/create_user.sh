#!/bin/sh
INSTALL_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $INSTALL_HOME

# Unzip package
SLOG=$INSTALL_HOME/log/sqlcl.log
LOG=$INSTALL_HOME/log/install.log

TNS_ADMIN=""
TNS_PROFILE=""
DB_USER=""
DB_PASSWORD=""
DB_SCHEMA=""
APEX_WORKSPACE=""
ADMIN_PASSWORD=""

print_usage()
{
    echo ""
    echo " create_user.sh [-d WALLET_DIR] [-t TNS_PROFILE] [-u DB_USER] [-p DB_PASSWORD] [-s DB_SCHEMA] [-w APEX_WORKSPACE] [-a ADMIN_PASSWORD] [-h]"
    echo ""
    echo " -d: Wallet Directory"
    echo " -t: TNS profile used to connect to database"
    echo " -u: Database User (to create)"
    echo " -p: Database Password (to create for Database User)"
    echo " -s: Database Schema (for Database User)"
    echo " -w: APEX Workspace (to install APEX applications)"
    echo " -a: ADMIN Password"
    echo " -h: this help"
    echo ""
}

while getopts 'd:t:u:p:s:w:a:h' flag; do
  case "${flag}" in
    d) export TNS_ADMIN="$(realpath ${OPTARG})" ;;
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
if [ -z "$TNS_ADMIN" ]
then
    read -p "Wallet Directory: " TNS_ADMIN
    export TNS_ADMIN="$(realpath ${TNS_ADMIN})"
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

# Run Commands
# Create DB User
# Install APEX apps
echo "set lines 199 trimsp on pages 0 feed on
-- spool $SLOG
connect ADMIN/\"${ADMIN_PASSWORD}\"@${TNS_PROFILE};
create user ${DB_USER} identified by \"${DB_PASSWORD}\";
grant DWROLE, CONNECT, RESOURCE, SODA_APP, unlimited tablespace to ${DB_USER};
grant create view to ${DB_USER};
grant create materialized view to ${DB_USER};
grant create procedure to ${DB_USER};
exec apex_instance_admin.add_workspace(p_workspace => '${APEX_WORKSPACE}', p_primary_schema => '${DB_SCHEMA}');
begin
apex_util.set_workspace(p_workspace => '${APEX_WORKSPACE}');
apex_util.create_user(
  p_user_name => '${DB_USER}',
  p_web_password => '${DB_PASSWORD}',
  p_developer_privs => 'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',
  p_email_address => '${DB_USER}@withoracle.cloud',
  p_default_schema => '${DB_SCHEMA}',
  p_change_password_on_first_use => 'N');
end;
/
" | $INSTALL_HOME/sqlcl/bin/sql /NOLOG
