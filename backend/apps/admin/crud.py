#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
# 注册API
from fastapi import APIRouter
from fastapi_amis_admin.crud import SqlalchemyCrud

from apps.admin.models.contractdetail import Contractdetail
from core.globals import site

from construct.app import App

from utils.log import log as log

router = APIRouter(prefix='/admin/contract')
#contractdetail_crud = SqlalchemyCrud(model=Contractdetail, engine=site.engine, pk_name='contractdetail_id').register_crud()
#site.router.include_router(contractdetail_crud.router)

