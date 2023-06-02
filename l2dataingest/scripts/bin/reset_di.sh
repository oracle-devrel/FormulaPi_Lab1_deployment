#!/bin/sh
echo "This will reset / restart the services."
sudo systemctl restart rabbitmq-server
sudp rabbitmqctl purge_queue PacketData
sudo systemctl restart f1sim-consumer
sudo systemctl restart f1sim-producer
