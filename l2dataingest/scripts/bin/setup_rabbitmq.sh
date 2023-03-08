#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
cd $F1SIM_HOME

print_usage()
{
    echo ""
    echo " setup_rabbitmq.sh [-u USERNAME] [-p PASSWORD] [-h]"
    echo ""
    echo " -u: for the RabbitMQ (remote) username"
    echo " -p: for the RabbitMQ (remote) password"
    echo " -h: this help"
    echo ""
}

while getopts 'u:p:h' flag; do
  case "${flag}" in
    u) RMQ_USER="${OPTARG}" ;;
    p) RMQ_PASS="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [ "${RMQ_USER}" = "" ]
then
    read -p "RabbitMQ User: " RMQ_USER
fi

if [ "${RMQ_PASS}" = "" ]
then
    stty -echo
    printf "RabbitMQ Password: "
    read RMQ_PASS
    stty echo
    printf "\n"
fi

KERNEL=`uname -s`
MACHINE=`uname -m`

sudo rabbitmqctl add_user "$RMQ_USER" "$RMQ_PASS"
sudo rabbitmqctl set_user_tags "$RMQ_USER" administrator
sudo rabbitmqctl set_permissions "$RMQ_USER" ".*" ".*" ".*"
sudo rabbitmq-plugins enable rabbitmq_management rabbitmq_mqtt rabbitmq_web_mqtt
if [ "$KERNEL" = "Linux" ]
then
    if [ "$MACHINE" = "x86_64" ]
    then
        sudo wget -P /usr/sbin http://localhost:15672/cli/rabbitmqadmin
        sudo chmod 755 /usr/sbin/rabbitmqadmin
    fi
fi
sudo rabbitmqadmin declare queue name="PacketData"
sudo rabbitmqadmin declare binding source="amq.topic" destination="PacketData"

echo "RabbitMQ User is configured."
echo "Ensure you update the f1store.yaml details (for the f1sim-web to access MQTT-WebSocket stream)."
