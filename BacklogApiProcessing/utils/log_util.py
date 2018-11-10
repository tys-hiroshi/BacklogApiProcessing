import logging.config

class LogUtil():
    def __init__(self):
        logging.config.fileConfig("logging_debug.conf")
        self.logger = logging.getLogger()
        pass

