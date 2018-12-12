import os
import logzero
from app import config

class log :

    def __init__(self) :
        self.logfile = os.path.join(config.logPath ,'unittest.log')
        logzero.logfile(self.logfile, maxBytes = 1e6, backupCount = 3)
        self.logger = logzero.logger


if __name__ == '__main__':
    input("You can not run main!")


