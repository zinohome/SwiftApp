#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from fastapi_amis_admin.admin import AdminApp
from starlette.requests import Request

from core.globals import site
from fastapi_amis_admin import amis, admin
from construct.app import App
from utils.log import log as log

appdef = App()
class AppHome(AdminApp):
    group_schema = 'Home'
    page_schema = amis.PageSchema(label='Home', title=f"{appdef.AppTitle}", icon='fa fa-bolt', sort=99)
    router_prefix = '/home'

    async def has_page_permission(self, request: Request) -> bool:
        return True
    def __init__(self, app: "AdminApp"):
        super().__init__(app)