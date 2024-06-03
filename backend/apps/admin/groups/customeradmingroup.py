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
from fastapi_amis_admin.crud import SqlalchemyCrud
from core.globals import site
from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp
from construct.app import App
from utils.log import log as log
from apps.admin.pages.customeradmin import CustomerAdmin

appdef = App()


class Customeradmingroup(admin.AdminApp):
    group_schema = 'Customer'
    page_schema = amis.PageSchema(label='客户管理', title='客户管理', icon='fa fa-bolt', sort=99)
    router_prefix = '/customer'


    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(CustomerAdmin)
