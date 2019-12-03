#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging.config

class Logger(object):
    def __init__(self, configFile):
        logging.config.fileConfig(configFile)
        self.logger = logging.getLogger()

    def info(self, message, console=False):
        if console:
            print(f'[I] {message}')
        self.logger.info(message)

    def debug(self, message, console=False):
        if console:
            print(f'[D] {message}')
        self.logger.debug(message)

if __name__ == '__main__':
    pass
