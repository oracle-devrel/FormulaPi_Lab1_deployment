import pika
from pika.exceptions import AMQPError
import os
import logging
from pathlib import Path
from f1sim import PacketWriter

home = str(Path.home())

class RabbitMQProducer(PacketWriter):

    def __init__(self, parameters):
        self.host = parameters['host']
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, heartbeat=600, blocked_connection_timeout=300))
        self.channel = self.connection.channel()
        # declare our queues
        # self.channel.queue_declare(queue='PacketData')
        logging.info("Sending to RabbitMQ@" + self.host);

    def close_pool(self):
        self.connection.close()
        logging.info('Connection pool closed.')

    def insert(self, location, parameters):
        retry = 3
        while retry > 0:
            try:
                data = parameters[0]
                if type(data).__name__.find("Packet") != -1:
                    packet = data.pack()
                else:
                    packet = data
                properties = pika.BasicProperties(headers={'location': location})
                self.channel.basic_publish(exchange='amq.topic', routing_key='', body=packet, properties=properties);
                return 1
            except AMQPError as amqper:
                logging.error(amqper)
                try:
                    self.connection.close()
                except:
                    pass
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, heartbeat=600, blocked_connection_timeout=300))
                self.channel = self.connection.channel()
                # declare our queues
                # self.channel.queue_declare(queue='PacketData')
                logging.info("Sending to RabbitMQ@" + self.host);
            except Exception as ex:
                logging.error(ex)
            except Error as er:
                logging.error(er)
            retry = retry - 1
            logging.error("retries failed")
