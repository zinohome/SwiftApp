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
from apps.admin.models.contractdetail import Contractdetail
from core.globals import site

from construct.app import App
from utils.famupdate._sqlalchemy import SqlalchemyCrud
from utils.log import log as log

router = APIRouter(prefix='/contract')
#self.pk_name: str = self.pk_name or self.model.__table__.primary_key.columns.keys()[0]
log.debug(Contractdetail.__table__.primary_key.columns.keys()[0])
pn = str = 'id' or Contractdetail.__table__.primary_key.columns.keys()[0]
log.debug(pn)
contractdetail_crud = SqlalchemyCrud(model=Contractdetail, engine=site.engine).register_crud()
#router.include_router(contractdetail_crud.router)

