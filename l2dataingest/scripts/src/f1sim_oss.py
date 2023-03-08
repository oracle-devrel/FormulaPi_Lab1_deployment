import sys
import os
import logging
from pathlib import Path
from f1sim import PacketWriter

from json import dumps
from time import sleep
import json

from kafka import KafkaProducer
import yaml

home = str(Path.home())

class OSSWriter(PacketWriter):
    def __init__(self, parameters):
        self.ossusername = parameters['ossusername']
        self.osspassword = parameters['osspassword']
        self.broker = parameters['bs_server']

        logging.debug('OSS Configuration')
        logging.debug(self.broker)
        logging.debug(self.ossusername)
        logging.debug(self.osspassword)
        logging.info("Sending to " + self.broker);

        self.producer = KafkaProducer(bootstrap_servers=self.broker,
                        security_protocol = 'SASL_SSL', sasl_mechanism = 'PLAIN',
                        sasl_plain_username = self.ossusername,
                        sasl_plain_password = self.osspassword,   
                        value_serializer=lambda x:
                        dumps(x).encode('utf-8'))
        logging.info('Connection successful.')

    def close_pool(self):
        self.producer.flush()
        self.producer.close()
        logging.info('Writer closed.')

    def insert(self, location, parameters):

        data = parameters[0]
        topic = location;
        
        retry = 3
        while retry > 0:
            try:
                self.producer.send(topic, value=json.loads(data))
                self.producer.flush()

                return 1
            except Exception as ex:
                logging.error(ex)
                retry = retry - 1
            
            logging.error(ex)
            return -1
        return 1