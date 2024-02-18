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

from apps.admin.models.contract import Contract
from apps.admin.pages.contractdetailadmin import ContractdetailAdmin
from apps.admin.swiftadmin import SwiftAdmin
from core.globals import site
from typing import List, Optional
from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD, TabsModeEnum, Form, AmisAPI, DisplayModeEnum, InputExcel, InputTable
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
        ocontractdetail = ContractdetailAdmin(self.app)
        ocontractdetailmodelparser = TableModelParser(ocontractdetail.model)
        ofields = [field for field in model_fields(ocontractdetail.schema_model).values() if
                   field.name != ocontractdetail.pk_name]
        oscope = request.scope.copy()
        oscope['path'] = '/admin/contract/ContractdetailAdmin'
        oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
        orequest = Request(oscope)
        columns, keys = [], {}
        for field in ofields:
            omodelfield = ocontractdetailmodelparser.get_modelfield(field)
            column = self.amis_parser.as_table_column(omodelfield)
            if await self.has_update_permission(request, None, None) and omodelfield.name in model_fields(
                    # type: ignore
                    ocontractdetail.schema_model
            ):
                if column.type == "switch":
                    column.disabled = False
                column.quickEdit = await self.get_column_quick_edit(orequest, omodelfield)
            keys[column.name] = "${" + column.label + "}"
            column.name = column.label
            columns.append(column)
        d_form = Form(
            api=AmisAPI(
                method="post",
                url=f"{ocontractdetail.router_path}/item",
                data={"&": {"$excel": keys}},
            ),
            name=CrudEnum.create,
            mode=DisplayModeEnum.normal,
            body=[
                InputTable(
                    name="excel",
                    showIndex=False,
                    columns=columns,
                    addable=False,
                    copyable=False,
                    editable=False,
                    removable=False,
                ),
            ],
        )
        detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=d_form)
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

            # 构建子表CRUD
            ocontractdetail = ContractdetailAdmin(self.app)
            ocontractdetailmodelparser = TableModelParser(ocontractdetail.model)
            ofields = [field for field in model_fields(ocontractdetail.schema_model).values() if field.name != ocontractdetail.pk_name]
            oscope = request.scope.copy()
            oscope['path'] = '/admin/contract/ContractdetailAdmin'
            oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
            orequest = Request(oscope)
            columns, keys = [], {}
            for field in ofields:
                omodelfield = ocontractdetailmodelparser.get_modelfield(field)
                column = self.amis_parser.as_table_column(omodelfield)
                if await self.has_update_permission(request, None, None) and omodelfield.name in model_fields(
                        # type: ignore
                        ocontractdetail.schema_model
                ):
                    if column.type == "switch":
                        column.disabled = False
                    column.quickEdit = await self.get_column_quick_edit(orequest, omodelfield)
                keys[column.name] = "${" + column.label + "}"
                column.name = column.label
                columns.append(column)
            d_form = Form(
                api=AmisAPI(
                    method="post",
                    url=f"{ocontractdetail.router_path}/item",
                    data={"&": {"$excel": keys}},
                ),
                name=CrudEnum.create,
                mode=DisplayModeEnum.normal,
                body=[
                    InputTable(
                        name="excel",
                        showIndex=False,
                        columns=columns,
                        addable=True,
                        copyable=True,
                        editable=True,
                        removable=True,
                    ),
                ],
            )
            detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=d_form)
            detailtabitem.disabled = True
            formtab.tabs.append(detailtabitem)

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
            ocontractdetail = ContractdetailAdmin(self.app)
            ocontractdetailmodelparser = TableModelParser(ocontractdetail.model)
            ofields = [field for field in model_fields(ocontractdetail.schema_model).values() if
                       field.name != ocontractdetail.pk_name]
            oscope = request.scope.copy()
            oscope['path'] = '/admin/contract/ContractdetailAdmin'
            oscope['raw_path'] = '/admin/contract/ContractdetailAdmin'
            orequest = Request(oscope)
            columns, keys = [], {}
            for field in ofields:
                omodelfield = ocontractdetailmodelparser.get_modelfield(field)
                column = self.amis_parser.as_table_column(omodelfield)
                if await self.has_update_permission(request, None, None) and omodelfield.name in model_fields(
                        # type: ignore
                        ocontractdetail.schema_model
                ):
                    if column.type == "switch":
                        column.disabled = False
                    column.quickEdit = await self.get_column_quick_edit(orequest, omodelfield)
                keys[column.name] = "${" + column.label + "}"
                column.name = column.label
                columns.append(column)
            d_form = Form(
                api=AmisAPI(
                    method="post",
                    url=f"{ocontractdetail.router_path}/item",
                    data={"&": {"$excel": keys}},
                ),
                name=CrudEnum.create,
                mode=DisplayModeEnum.normal,
                body=[
                    InputTable(
                        name="excel",
                        showIndex=False,
                        columns=columns,
                        addable=True,
                        copyable=True,
                        editable=True,
                        removable=True,
                    ),
                ],
            )
            detailtabitem = amis.Tabs.Item(title=_('合同明细'), tab=d_form)
            detailtabitem.disabled = False
            formtab.tabs.append(detailtabitem)

            u_form.body = formtab
        return u_form
