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
import fastapi_amis_admin.admin.admin as file_admin
import fastapi_amis_admin.crud._sqlalchemy as file_sqlalchemy
import fastapi_user_auth.admin.site as file_site
import fastapi_user_auth.auth.models as file_models

from utils.log import log as log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEF_DIR = os.path.join(BASE_DIR, 'construct')

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
class Modelchecker():

    def check_models(self):
        # 定义文件目录 backend/construct
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        # 应用目录 backend
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        # 运行目录 backend/construct/update
        updatepath = os.path.abspath(os.path.join(apppath, 'construct/update'))
        log.debug("Check models Starting ...")
        try:
            log.debug(updatepath)
        except Exception as exp:
            print('Exception at Modelchecker.check_models() %s ' % exp)
            traceback.print_exc()

    if __name__ == '__main__':
        log.debug(file_admin.__file__)
        log.debug(file_sqlalchemy.__file__)
        log.debug(file_site.__file__)
        log.debug(file_models.__file__)
