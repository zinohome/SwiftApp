#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from apps.admin.models.contract import Contract
from apps.admin.swiftadmin import SwiftAdmin
from core.globals import site
from typing import List, Optional
from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD, TabsModeEnum, Form
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class ContractAdmin(SwiftAdmin):
    group_schema = None
    page_schema = PageSchema(label='合同管理', page_title='合同管理', icon='fa fa-border-all')
    model = Contract
    pk_name = 'contract_id'
    list_display = [Contract.contract_id, Contract.contact_number, Contract.contact_type, Contract.customer_name, Contract.supplier_name, Contract.sign_date, Contract.sign_address, Contract.delivery_data]
    search_fields = []
    tabsMode = TabsModeEnum.card

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.action_type = 'Drawer'

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs = []
            fieldlist = []
            for item in c_form.body:
                fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('基本信息'), tab=fieldlist)
            detailtabitem = amis.Tabs.Item(title=_('合同明细'))
            detailtabitem.disabled = True
            formtab.tabs.append(basictabitem)
            formtab.tabs.append(detailtabitem)
            c_form.body = formtab
            log.debug(c_form.json)
        return c_form


