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
import shutil
import fastapi_amis_admin.admin.admin as file_admin
import fastapi_amis_admin.crud._sqlalchemy as file_sqlalchemy
import fastapi_amis_admin.crud.parser as file_parser
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
            for tfile in (file_admin, file_sqlalchemy, file_parser, file_site, file_models):
                with open(tfile.__file__, "r") as rfile:
                    fline = rfile.readline()[0:12]
                    if fline != "#  @Software":
                        match tfile.__name__.split('.')[-1]:
                            case "admin":
                                if os.path.exists(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/admin/admin.py'))):
                                    log.debug("Check model: %s ..." %tfile.__file__)
                                    shutil.copy(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/admin/admin.py')),
                                        tfile.__file__)
                            case "_sqlalchemy":
                                if os.path.exists(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/crud/_sqlalchemy.py'))):
                                    log.debug("Check model: %s ..." % tfile.__file__)
                                    shutil.copy(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/crud/_sqlalchemy.py')),
                                        tfile.__file__)
                            case "parser":
                                if os.path.exists(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/crud/parser.py'))):
                                    log.debug("Check model: %s ..." % tfile.__file__)
                                    shutil.copy(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_amis_admin/crud/parser.py')),
                                        tfile.__file__)
                            case "site":
                                if os.path.exists(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_user_auth/admin/site.py'))):
                                    log.debug("Check model: %s ..." % tfile.__file__)
                                    shutil.copy(
                                        os.path.abspath(
                                            os.path.join(updatepath, 'fastapi_user_auth/admin/site.py')),
                                        tfile.__file__)
                            case "models":
                                if os.path.exists(
                                        os.path.abspath(os.path.join(updatepath, 'fastapi_user_auth/auth/models.py'))):
                                    log.debug("Check model: %s ..." % tfile.__file__)
                                    shutil.copy(
                                        os.path.abspath(
                                            os.path.join(updatepath, 'fastapi_user_auth/auth/models.py')),
                                        tfile.__file__)
                        #if os.path.exists(test_file.txt)
            log.debug("Check models completed ！")
        except Exception as exp:
            print('Exception at Modelchecker.check_models() %s ' % exp)
            traceback.print_exc()

if __name__ == '__main__':
    mc = Modelchecker()
    #mc.check_models()
