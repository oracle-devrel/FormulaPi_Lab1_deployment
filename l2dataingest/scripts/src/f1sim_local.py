import os
import logging
from pathlib import Path
from f1sim import PacketWriter
import time
import pickle 
import json
import yaml

home = str(Path.home())

class FileWriter(PacketWriter):
    def __init__(self, parameters):
        self.filedir = parameters['filedir']
        self.filetype = parameters['filetype']
        # Check whether the specified path exists or not
        if os.path.exists(self.filedir) == False:
            # Create a new directory because it does not exist 
            os.makedirs(self.filedir)
        logging.debug(self.filedir)
        logging.info('Writer created.')
        with open('f1store.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
        self.FILTER_DATA = config['filter']

    def close_pool(self):
        logging.info('Writer closed.')

    def insert(self, location, parameters):
        try:
            filedir = self.filedir
            filetype = self.filetype
            timestamp = time.time_ns() 
            data = parameters[0]
            session = data.m_header.m_session_uid;
            if os.path.exists(self.filedir+'/'+str(session)) == False:
                # Create a new directory because it does not exist 
                os.makedirs(self.filedir+'/'+str(session))
            packet_id = location;
            with open(f'{filedir}/{session}/{session}-{packet_id}-{timestamp}.{filetype}', 'wb') as fh:
                if filetype == 'pickle':
                    pickle.dump(data, fh, protocol=pickle.HIGHEST_PROTOCOL)
                elif filetype == 'bytes':
                    fh.write(data.pack())
        except Exception as ex:
            logging.error(ex)
            return -1
        return 1

