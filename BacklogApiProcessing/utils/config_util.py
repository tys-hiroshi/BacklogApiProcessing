# -*- coding: utf-8 -*-
import io
import yaml

class ConfigUtil():
    def __init__(self):
        pass

    def read_yaml_file(self, filePath):
        with open(filePath, "r", encoding="utf-8") as yml:
            return yaml.load(yml)