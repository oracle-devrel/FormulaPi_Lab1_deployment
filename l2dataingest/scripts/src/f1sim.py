import os
import logging
import importlib
from pathlib import Path

class PacketWriter:

    def __init__(self, parameters):
        pass

    def close_pool(self):
        pass

    def insert(self, location, parameters):
        pass


def loadclass(fullclassname):
    if fullclassname.rfind('.') > 1:
        modulename = fullclassname[:fullclassname.rfind('.')]
        classname = fullclassname[fullclassname.rfind('.')+1:]
        logging.info('Loading '+fullclassname)       
        m = importlib.import_module(modulename)
        return getattr(m, classname)
    raise ValueError
