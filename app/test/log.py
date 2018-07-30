import platform
import logzero
from app import config

class log :

    def __init__(self) :
        if platform.system() == 'Windows':
            self.logfile = config.logPath + '\\' + 'unittest.log'
        else:
            self.logfile = '/opt/flask/flask/log/unittest.log'
        logzero.logfile(self.logfile, maxBytes = 1e6, backupCount = 3)
        self.logger = logzero.logger


if __name__ == '__main__':
    input("You can not run main!")


