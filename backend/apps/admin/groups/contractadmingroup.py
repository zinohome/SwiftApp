#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from apps.admin.pages.contractadmin import ContractAdmin
from core.globals import site
from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp
from construct.app import App
from ujtils.log import log as log

appdef = App()
class Contractadmingroup(admin.AdminApp):
    group_schema = 'Contract'
    page_schema = amis.PageSchema(label='Contract', title=f"{appdef.AppTitle}", icon='fa fa-bolt', sort=98)
    router_prefix = '/contract'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(ContractAdmin)