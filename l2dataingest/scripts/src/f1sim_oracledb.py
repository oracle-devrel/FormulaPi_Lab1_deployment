import cx_Oracle
import sys
import os
import logging
from pathlib import Path
from f1sim import PacketWriter

home = str(Path.home())

class OracleDatabaseConnection(PacketWriter):
    def __init__(self, parameters):
        if sys.platform == 'win32':
            cx_Oracle.init_oracle_client(lib_dir=os.getenv('ORACLE_HOME'))
        self.dbusername = parameters['dbusername']
        self.dbpassword = parameters['dbpassword']
        self.poolsize = parameters['poolsize']
        self.dburl = parameters['dburl']
        logging.debug(os.getenv("TNS_ADMIN"))
        logging.debug(self.dburl)
        logging.debug(self.dbusername)
        logging.debug(self.dbpassword)
        logging.debug(self.poolsize)
        logging.info("Sending to " + self.dbusername+"@"+self.dburl);
        self.pool = cx_Oracle.SessionPool(self.dbusername, self.dbpassword, self.dburl, min=self.poolsize, max=self.poolsize, increment=1, threaded=True,getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT)
        self.pool.ping_interval = 120
        self.pool.timeout = 600
        logging.info('Connection successful.')

    def close_pool(self):
        self.pool.close()
        logging.info('Connection pool closed.')

    def insert(self, location, parameters):
        connection = None
        retry = 3
        while retry > 0:
            try:
                connection = self.pool.acquire()
                connection.autocommit = True
                cursor = cx_Oracle.Cursor(connection)
                cursor.execute(location,parameters);
                return 1
            except Exception as ex:
                logging.error(ex)
                retry = retry - 1
            finally:
                if connection != None:
                    self.pool.release(connection)
            logging.error("retries failed")

def test_class():
    parameters = { "dbusername" : "username", "dbpassword" : "password", "dburl" : "url" };
    object = OracleDatabaseConnection(parameters)
    logging.info(object.pool)
    object.close_pool()

if __name__ == '__main__':
    test_class()
