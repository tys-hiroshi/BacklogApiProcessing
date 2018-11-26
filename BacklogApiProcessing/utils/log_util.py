# -*- coding: utf-8 -*-
import logging.config

class LogUtil():
    def __init__(self):
        logging.config.fileConfig("logging_debug.conf")
        self.logger = logging.getLogger()

    def info(self, msg):
        self.logger.info(msg)
        print(msg)
