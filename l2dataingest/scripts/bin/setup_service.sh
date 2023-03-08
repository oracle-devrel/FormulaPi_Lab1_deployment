#!/bin/sh

F1SIM_HOME=$(dirname $0 | xargs -I {} realpath {} | rev | cut -d '/' -f 2- | rev)
USER=$(whoami)

if [ ! -d /run/systemd/system ]
then
    echo "systemd is not available. start F1Sim manually" 
    echo "$ sudo /usr/lib/rabbitmq/bin/rabbitmq-server > rabbitmq-server.log 2>&1 &" 
    echo "$ ${F1SIM_HOME}/bin/run_producer.sh > run_producer.log 2>&1 &" 
    echo "$ ${F1SIM_HOME}/bin/run_consumer.sh > run_consumer.log 2>&1 &" 
    echo "$ ${F1SIM_HOME}/bin/run_webserver.sh &" 
    exit 1
fi

cp $F1SIM_HOME/bin/producer.service.template $F1SIM_HOME/bin/producer.service
cp $F1SIM_HOME/bin/consumer.service.template $F1SIM_HOME/bin/consumer.service
cp $F1SIM_HOME/bin/webserver.service.template $F1SIM_HOME/bin/webserver.service
cp $F1SIM_HOME/bin/healthcheck.cron.template $F1SIM_HOME/bin/healthcheck.cron

F1SIM_HOME_ESC=$(echo $F1SIM_HOME | sed 's_/_\\/_g')
sed -i "s/<F1SIM_HOME>/${F1SIM_HOME_ESC}/g" $F1SIM_HOME/bin/producer.service
sed -i "s/<USER>/${USER}/g" $F1SIM_HOME/bin/producer.service
sed -i "s/<F1SIM_HOME>/${F1SIM_HOME_ESC}/g" $F1SIM_HOME/bin/consumer.service
sed -i "s/<USER>/${USER}/g" $F1SIM_HOME/bin/consumer.service
sed -i "s/<F1SIM_HOME>/${F1SIM_HOME_ESC}/g" $F1SIM_HOME/bin/webserver.service
sed -i "s/<USER>/${USER}/g" $F1SIM_HOME/bin/webserver.service
sed -i "s/<F1SIM_HOME>/${F1SIM_HOME_ESC}/g" $F1SIM_HOME/bin/healthcheck.cron
sed -i "s/<USER>/${USER}/g" $F1SIM_HOME/bin/healthcheck.cron

KERNEL=`uname -s`
MACHINE=`uname -m`

BINDSVC=
if [ "$KERNEL" = "Linux" ]
then
    if [ "$MACHINE" = "aarch64" ]
    then
        BINDSVC="ln"
    elif [ "$MACHINE" = "x86_64" ]
    then
        BINDSVC="cp"
        sudo semanage fcontext -a -t bin_t "$F1SIM_HOME/bin.*"
        sudo chcon -Rv -u system_u -t bin_t "$F1SIM_HOME/bin"
    fi
fi

cd /lib/systemd/system
if [ -f f1sim-producer.service ]
then
    sudo rm f1sim-producer.service
fi
sudo ${BINDSVC} $F1SIM_HOME/bin/producer.service f1sim-producer.service
if [ -f f1sim-consumer.service ]
then
    sudo rm f1sim-consumer.service
fi
sudo ${BINDSVC} $F1SIM_HOME/bin/consumer.service f1sim-consumer.service
if [ -f f1sim-webserver.service ]
then
    sudo rm f1sim-webserver.service
fi
sudo ${BINDSVC} $F1SIM_HOME/bin/webserver.service f1sim-webserver.service
sudo systemctl daemon-reload
sudo systemctl enable f1sim-webserver

# legacy cron installation
cd /etc/cron.d
if [ -f f1sim-healthcheck ]
then
    sudo rm f1sim-healthcheck
fi

cd $F1SIM_HOME/bin
crontab -l > crontab.tmp
grep -v "healthcheck.sh" crontab.tmp > crontab.txt
rm crontab.tmp
crontab crontab.txt

crontab -l > crontab.txt
cat healthcheck.cron >> crontab.txt
crontab crontab.txt

echo "Linked producer and consumer services to systemd"
echo "Start F1Sim Producer: systemctl start f1sim-producer"
echo "Start F1Sim Consumer: systemctl start f1sim-consumer"
echo "Start F1Sim WebServer: systemctl start f1sim-webserver"
