#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import yaml

class Config(object):
    def __init__(self, ymlFile):
        with open(ymlFile, 'r', encoding='utf-8') as f:
            self.content = yaml.safe_load(f)

if __name__ == '__main__':
    pass
