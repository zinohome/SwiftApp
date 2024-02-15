#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

from sqlalchemy_database import AsyncDatabase, Database

from core.settings import settings

# 创建异步数据库引擎
async_db = AsyncDatabase.create(
    url=settings.database_url_async,
    session_options={
        "expire_on_commit": False,
    },
)
# 创建同步数据库引擎
sync_db = Database.create(
    url=settings.database_url,
    session_options={
        "expire_on_commit": False,
    },
)


from fastapi_amis_admin.admin import AdminSite

site = AdminSite(settings, engine=async_db)



