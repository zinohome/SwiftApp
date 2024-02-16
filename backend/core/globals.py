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
from typing import Optional

from fastapi import FastAPI
from fastapi_amis_admin.admin import HomeAdmin, DocsAdmin, ReDocsAdmin
from fastapi_amis_admin.amis import App, ActionType, Flex, Drawer, SizeEnum, Service, AmisAPI, InputImage, ColumnImage
from fastapi_amis_admin.crud.utils import SqlalchemyDatabase
from fastapi_user_auth.admin import AuthAdminSite
from fastapi_user_auth.auth import Auth
from fastapi_user_auth.auth.schemas import SystemUserEnum
from sqlalchemy_database import AsyncDatabase, Database
from fastapi_user_auth.auth.backends.jwt import JwtTokenStore
from starlette.requests import Request
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.auth.models import BaseUser

from core.settings import settings, Settings
from utils.log import log as log
from core import i18n as _

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

auth = Auth(db=async_db, token_store=JwtTokenStore(secret_key=settings.secret_key))
site = AuthAdminSite(settings, engine=async_db, auth=auth)
auth = site.auth
site.UserAuthApp.page_schema.sort = -99






