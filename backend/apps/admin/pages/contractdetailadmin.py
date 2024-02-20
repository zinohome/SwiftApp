#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from fastapi_amis_admin.admin import PageAdmin, ModelAdmin
from sqlalchemy import Select

from apps.admin.models.contract import Contract
from apps.admin.models.contractdetail import Contractdetail
from apps.admin.swiftadmin import SwiftAdmin
from core.globals import site
from typing import List, Optional, TYPE_CHECKING
from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD, Page, TabsModeEnum
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class ContractdetailAdmin(SwiftAdmin):
    group_schema = None
    page_schema = PageSchema(label='合同明细', page_title='合同明细', icon='fa fa-border-all')
    model = Contractdetail
    pk_name = 'contractdetail_id'
    list_per_page = 50
    list_display = []
    search_fields = []
    parent_class = "ContractAdmin"
    tabsMode = TabsModeEnum.card
    detail_mode = True


    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # 启用批量新增
        self.enable_bulk_create = False
        # 启用查看
        self.schema_read = None
        # 设置form弹出类型  Drawer | Dialog
        self.action_type = 'Dialog'


    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        log.debug(self.detail_mode)
        log.debug(sel.filter(Contractdetail.contract_id == 1))
        return sel.filter(Contractdetail.contract_id == 1)