#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from fastapi_amis_admin.crud import CrudEnum
from fastapi_amis_admin.crud.parser import TableModelParser
from fastapi_amis_admin.utils.pydantic import model_fields
from pydantic._internal._decorators import mro

from apps.admin.models.contract import Contract
from apps.admin.pages.contractdetailadmin import ContractdetailAdmin
from apps.admin.swiftadmin import SwiftAdmin
from core.globals import site
from typing import List, Optional
from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD, TabsModeEnum, Form, AmisAPI, DisplayModeEnum, InputExcel, InputTable, Page
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class ContractAdmin(SwiftAdmin):
    group_schema = None
    page_schema = PageSchema(label='合同管理', page_title='合同管理', icon='fa fa-border-all')
    model = Contract
    pk_name = 'contract_id'
    list_per_page = 50
    list_display = [Contract.contract_id, Contract.contact_number, Contract.contact_type, Contract.customer_name, Contract.supplier_name, Contract.sign_date, Contract.sign_address, Contract.delivery_data]
    search_fields = []
    parent_class = None
    tabsMode = TabsModeEnum.card

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # 启用批量新增
        self.enable_bulk_create = False
        # 启用查看
        self.schema_read = self.schema_model
        # 设置form弹出类型  Drawer | Dialog
        self.action_type = 'Drawer'

    async def get_read_form(self, request: Request) -> Form:
        r_form = await super().get_read_form(request)
        # 构建主表Read
        formtab = amis.Tabs(tabsMode='line')
        formtab.tabs = []
        fieldlist = []
        for item in r_form.body:
            if item.name != self.pk_name:
                fieldlist.append(item)
        basictabitem = amis.Tabs.Item(title=_('基本信息'), tab=fieldlist)
        formtab.tabs.append(basictabitem)

        # 构建子表CRUD
        oscope = request.scope.copy()
        oscope['path'] = '/admin/contract/ContractdetailAdmin'
        oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
        orequest = Request(oscope)
        contractdetailadmin = ContractdetailAdmin(self.app)
        table =await self.get_sub_list_table(contractdetailadmin, orequest)
        headerToolbar = [
            {"type": "columns-toggler", "align": "left", "draggable": False},
            {"type": "reload", "align": "right"}
        ]
        table.headerToolbar = headerToolbar
        table.itemActions = None
        detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=table)
        detailtabitem.disabled = False
        formtab.tabs.append(detailtabitem)

        r_form.body = formtab
        return r_form

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            # 构建主表Create
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs = []
            fieldlist = []
            for item in c_form.body:
                fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('基本信息'), tab=fieldlist)
            formtab.tabs.append(basictabitem)
            '''
            # 构建子表CRUD
            oscope = request.scope.copy()
            oscope['path'] = '/admin/contract/ContractdetailAdmin'
            oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
            orequest = Request(oscope)
            contractdetailadmin = ContractdetailAdmin(self.app)
            table =await self.get_sub_list_table(contractdetailadmin, orequest)
            detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=table)
            detailtabitem.disabled = True
            formtab.tabs.append(detailtabitem)
            '''
            c_form.body = formtab
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request, bulk)
        if not bulk:
            # 构建主表Update
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs = []
            fieldlist = []
            for item in u_form.body:
                fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('基本信息'), tab=fieldlist)
            detailtabitem = amis.Tabs.Item(title=_('合同明细'))
            detailtabitem.disabled = False
            formtab.tabs.append(basictabitem)

            # 构建子表CRUD
            oscope = request.scope.copy()
            oscope['path'] = '/admin/contract/ContractdetailAdmin'
            oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
            orequest = Request(oscope)
            contractdetailadmin = ContractdetailAdmin(self.app)
            table =await self.get_sub_list_table(contractdetailadmin, orequest)
            detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=table)
            detailtabitem.disabled = False
            formtab.tabs.append(detailtabitem)

            u_form.body = formtab
        return u_form

    async def get_page(self, request: Request) -> Page:
        log.debug(await super().get_page(request))
        return await super().get_page(request)