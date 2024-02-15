#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp
from construct.app import App
from ujtils.log import log as log

# from .models import Category

app = App()
class AppHome(admin.AdminApp):
    page_schema = amis.PageSchema(label='Home', title=f"{app.AppTitle}", icon='fa fa-bolt', sort=99)
    router_prefix = '/home'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)

