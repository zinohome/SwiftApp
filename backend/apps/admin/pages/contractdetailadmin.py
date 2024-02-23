#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
import traceback

from fastapi_amis_admin.admin import PageAdmin, ModelAdmin
from fastapi_amis_admin.crud.base import SchemaCreateT, SchemaUpdateT
from fastapi_amis_admin.crud.parser import TableModelT
from sqlalchemy import Select, update, text
from sqlmodel import Session, select

from apps.admin.models.contract import Contract
from apps.admin.models.contractdetail import Contractdetail
from apps.admin.swiftadmin import SwiftAdmin
from core.globals import site
from typing import List, Optional, TYPE_CHECKING, Dict, Union, Any
from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD, Page, TabsModeEnum
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class ContractdetailAdmin(SwiftAdmin):
    group_schema = None
    page_schema = PageSchema(label='合同明细', page_title='合同明细', icon='fa fa-border-all', sort=97)
    model = Contractdetail
    pk_name = 'contractdetail_id'
    list_per_page = 50
    list_display = [Contractdetail.contract_id, Contractdetail.item_number, Contractdetail.item_name, Contractdetail.item_spec, Contractdetail.item_quantity, Contractdetail.unit_price, Contractdetail.item_mount]
    search_fields = [Contractdetail.contract_id, Contractdetail.item_number, Contractdetail.item_name, Contractdetail.item_spec, Contractdetail.item_quantity, Contractdetail.unit_price, Contractdetail.item_mount]
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
        self.action_type = 'Drawer'

    async def on_create_pre(self, request: Request, obj: SchemaCreateT, **kwargs) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj)
        data['item_mount'] = data['item_quantity']*data['unit_price']
        return data

    async def on_update_pre(
            self,
            request: Request,
            obj: SchemaUpdateT,
            item_id: Union[List[str], List[int]],
            **kwargs,
    ) -> Dict[str, Any]:
        data = await super().on_update_pre(request, obj, item_id)
        data['item_mount'] = data['item_quantity']*data['unit_price']
        return data

    async def update_items(self, request: Request, item_id: List[str], values: Dict[str, Any]) -> List[TableModelT]:
        try:
            result = await super().update_items(request, item_id, values)
            if len(result) > 0:
                #UPDATE `contract` SET contract_amount = ( SELECT SUM(item_mount) FROM contractdetail WHERE contractdetail.contract_id = 1 ) WHERE contract.contract_id = 1;
                #statement = select(Contract).where(Contract.contract_id == values['contract_id'])
                statement = text("UPDATE contract SET contract_amount = ( SELECT SUM(item_mount) FROM contractdetail WHERE contractdetail.contract_id = :contract_id ) WHERE contract.contract_id = :contract_id")
                uresult = await self.app.db.async_execute(statement,{'contract_id':values['contract_id']})
                #log.debug(uresult)
            return result
        except Exception as exp:
            print('Exception at Appdef.readconfig() %s ' % exp)
            traceback.print_exc()

