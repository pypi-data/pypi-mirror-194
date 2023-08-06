#myLog.py
import logging, getpass, time
from pathlib import Path

class Log(object):
    #class CALog(logging.Logger):
# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
    def __init__(self):
        user=getpass.getuser()
        FORMAT='%(asctime)s-%(levelname)s: %(message)s'

        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        
        formatter=logging.Formatter(FORMAT, datefmt='%Y%m%d-%H%M%S')
        streamhandler=logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)

        log_path = Path(__file__).parent.parent / "logs"
        log_path.mkdir(parents=True, exist_ok=True)

        logfilename= user + time.strftime("-%Y-%b") + '.log'
        logfile = log_path / logfilename
        filehandler=logging.FileHandler(logfile, encoding="utf-8")
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)
    def critical(self, msg):
        self.logger.critical(msg)
    def log(self, level, msg):
        self.logger.log(level, msg)
    def setLevel(self, level):
        self.logger.setLevel(level)
    def disable(self):
        logging.disable(50)