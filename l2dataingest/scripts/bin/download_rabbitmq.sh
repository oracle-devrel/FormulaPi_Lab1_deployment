#!/bin/sh

KERNEL=`uname -s`
MACHINE=`uname -m`

echo "Installing for $KERNEL $MACHINE"
if [ "$KERNEL" = "Linux" ]
then
    if [ "$MACHINE" = "aarch64" ]
    then
        sudo apt-get install rabbitmq-server
        sudo systemctl enable rabbitmq-server
        sudo systemctl start rabbitmq-server
    elif [ "$MACHINE" = "x86_64" ]
    then
        mkdir $HOME/Downloads
        wget -P $HOME/Downloads https://github.com/rabbitmq/erlang-rpm/releases/download/v25.1.2/erlang-25.1.2-1.el8.x86_64.rpm
        wget -P $HOME/Downloads https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.11.3/rabbitmq-server-3.11.3-1.el8.noarch.rpm
        sudo yum install -y socat logrotate
        sudo yum install -y $HOME/Downloads/erlang-25.1.2-1.el8.x86_64.rpm
        sudo yum install -y $HOME/Downloads/rabbitmq-server-3.11.3-1.el8.noarch.rpm
        sudo chkconfig rabbitmq-server on
        sudo systemctl daemon-reload
        sudo systemctl start rabbitmq-server.service
    else
        echo "$KERNEL $MACHINE not found"
        echo "Install rabbitmq manually if supported by platform"
        exit 1
    fi
else
    echo "$KERNEL $MACHINE not found"
    echo "Install rabbitmq manually if supported by platform"
    exit 1
fi
