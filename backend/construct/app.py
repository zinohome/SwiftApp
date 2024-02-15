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
DEF_DIR = os.path.join(BASE_DIR, 'construct')
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
class App():
    def __init__(self):
        self.AppName = None
        self.AppTitle = None
        self.Description = None
        self.Version = None
        self.Author = None
        self.Cons = None
        self.Consdict = None
        self.readconfig()

    def readconfig(self):
        try:
            with open(DEF_PATH, 'r', encoding="utf-8") as app_file:
                content = app_file.read()
            app_obj = json.loads(content, object_hook=obj)
            self.AppName = app_obj.AppName
            self.AppTitle = app_obj.AppTitle
            self.Description = app_obj.Description
            self.Version = app_obj.Version
            self.Author = app_obj.Author
            self.Cons = app_obj
            appdict = json.loads(content)
            self.Consdict = appdict
        except Exception as exp:
            print('Exception at Appdef.readconfig() %s ' % exp)
            traceback.print_exc()


if __name__ == '__main__':
    app = App()
    print(app.AppName)
    print(app.Cons.Settings)
    print(app.Cons.Settings.language)
    print(app.Consdict)
    print(app.Cons.DBConnecton.Type)