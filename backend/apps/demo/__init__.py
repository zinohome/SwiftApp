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


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    # 导入相关模块
    from . import admin, apis, jobs

    # 注册路由
    router.include_router(apis.router, prefix='/demo', tags=['Demo'])
    # 注册管理页面
    admin_app.register_admin(admin.DemoApp)

