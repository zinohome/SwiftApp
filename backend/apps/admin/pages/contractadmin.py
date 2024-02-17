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
from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _

class ContractAdmin(SwiftAdmin):
    group_schema = None
    page_schema = PageSchema(label='合同管理', page_title='合同管理', icon='fa fa-border-all')
    model = Contract
    pk_name = 'contract_id'
    pk_label = 'contact_number'
    list_display = [Contract.contract_id, Contract.contact_number, Contract.contact_type, Contract.customer_name, Contract.supplier_name, Contract.sign_date, Contract.sign_address, Contract.delivery_data]
    search_fields = []

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.action_type = 'Drawer'

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list
