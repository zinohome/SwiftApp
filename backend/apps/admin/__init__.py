#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp

from apps.admin.groups import apphome, contractadmingroup


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    # 导入相关模块
    from . import admin, apis, jobs, crud

    # 注册路由
    #router.include_router(apis.router, prefix='/home', tags=['Home'])
    router.include_router(apis.router)
    router.include_router(crud.router)
    # 注册管理页面
    #admin_app.register_admin(apphome.AppHome)
    #admin_app.register_admin(contractadmin.Contractadmingroup)

