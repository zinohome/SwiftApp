#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
import importlib
import inspect
import os

from apps.admin.groups.apphome import AppHome
from apps.admin.groups.contractadmingroup import Contractadmingroup
from apps.admin.groups.customeradmingroup import Customeradmingroup
from core.globals import site
from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp
from construct.app import App
from utils.log import log as log
from utils.modelchecker import Modelchecker

# 更新系统库文件
mc = Modelchecker()
mc.check_models()

appdef = App()


# 定义文件目录 backend/apps/admin
basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
# 应用目录 backend/apps
apppath = os.path.abspath(os.path.join(basepath, os.pardir))
# 运行目录 backend/apps/groups
grouppath = os.path.abspath(os.path.join(apppath, 'admin/groups'))

items = os.scandir(grouppath)
for file in items:
    if file.is_file() and file.name != '__init__.py':
        module_name = 'apps.admin.groups.' + os.path.splitext(file.name)[0]
        adminmodel = importlib.import_module(module_name)
        for name, class_ in inspect.getmembers(adminmodel, inspect.isclass):
            if name.lower() == os.path.splitext(file.name)[0]:
                log.debug("Regist admin module [ %s ] ..." % name)
                site.register_admin(class_)

#site.register_admin(AppHome)
#site.register_admin(Contractadmingroup, Customeradmingroup)


