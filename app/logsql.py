import os
import logzero
from app import config

class log :

    def __init__(self) :
        self.logfile = os.path.join(config.logPath, 'sql.log')
        logzero.logfile(self.logfile, maxBytes = 1e6, backupCount = 3)
        import logging
        formatter = logging.Formatter('%(asctime)-15s - [%(filename)s: %(lineno)s] -%(levelname)s: %(message)s');
        logzero.formatter(formatter)
        self.logger = logzero.logger


if __name__ == '__main__':
    input("You can not run main!")


