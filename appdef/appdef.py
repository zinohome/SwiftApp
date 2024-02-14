#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

import os
import traceback
from utils.log import log as log
import simplejson as json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF_DIR = os.path.join(BASE_DIR, 'appdef')
DEF_PATH = os.path.join(DEF_DIR, 'app.json')

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class Appdef():
    def __init__(self):
        self.AppName = None
        self.Config = None
        self.DBConnecton =None
        self.readconfig()

    def readconfig(self):
        try:
            with open(DEF_PATH, 'r') as appdef_file:
                appdef_data = json.load(appdef_file, object_hook=obj)
                self.AppName = appdef_data.AppName
                self.Config = appdef_data.Config
                self.DBConnecton = appdef_data.DBConnecton
        except Exception as exp:
            log.error('Exception at Appdef.readconfig() %s ' % exp)
            traceback.print_exc()


if __name__ == '__main__':
    appdef = Appdef()
    log.debug(appdef.AppName)
    log.debug(appdef.Config)
    log.debug(appdef.DBConnecton.Type)