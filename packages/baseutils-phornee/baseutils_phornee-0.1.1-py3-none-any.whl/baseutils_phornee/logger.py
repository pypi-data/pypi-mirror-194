import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import time
from enum import Enum

class Logger_Mode(Enum):
    NONE=0
    FILE=1
    STD=2
    BOTH=3

class UTCFormatter(logging.Formatter):
    converter = time.gmtime


class Logger:

    def __init__(self, package_name: str,  
                       log_file_name: str, 
                       mode: Logger_Mode = Logger_Mode.FILE, 
                       level = logging.INFO, 
                       utc: bool = False):
        self.log_file_name = log_file_name

        self.homevar = os.path.join(str(Path.home()), 'var', 'log', package_name)
        self.package_name = package_name

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.setupLogger(mode, level, utc)

    def getLogPath(self) -> str:
        return os.path.join(self.homevar, "{}.log".format(self.log_file_name))

    def setupLogger(self, mode: Logger_Mode, level, utc: bool):
        self.logger = logging.getLogger('{}_{}_log'.format( self.package_name, self.log_file_name))

        if not os.path.exists( self.homevar):
            os.mkdir( self.homevar)

        if utc:
            formatter = UTCFormatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')
        else:
            formatter = logging.Formatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')

        # Create rotating file handler
        if mode in [Logger_Mode.FILE, mode.BOTH]:
            fh = RotatingFileHandler(self.getLogPath(), maxBytes=10000, backupCount=10)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        # Create stdout stream handler
        if mode in [Logger_Mode.STD, mode.BOTH]:
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)

        # Create empty log file if it doesn´t previously exist
        if not os.path.exists(self.getLogPath()):
            with open(self.getLogPath(), 'w'):
                pass
                
        # Same level in both handlers
        self.logger.setLevel(level)

    def getLog(self) -> str:
        with open(self.getLogPath(), 'r') as file:
            return file.read()

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

