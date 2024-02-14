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
        self.Def = None
        self.Defdict = None
        self.readconfig()

    def readconfig(self):
        try:
            with open(DEF_PATH, 'r', encoding="utf-8") as appdef_file:
                defcontent = appdef_file.read()
            appdef_obj = json.loads(defcontent, object_hook=obj)
            self.AppName = appdef_obj.AppName
            self.Def = appdef_obj
            appdef = json.loads(defcontent)
            self.Defdict = appdef
        except Exception as exp:
            print('Exception at Appdef.readconfig() %s ' % exp)
            traceback.print_exc()


if __name__ == '__main__':
    appdef = Appdef()
    print(appdef.AppName)
    print(appdef.Def.Config)
    print(appdef.Def.DBConnecton.Type)
    print(appdef.Defdict)
    print(appdef.Def.Config.api_prefix[1:])