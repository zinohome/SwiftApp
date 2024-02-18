#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
import asyncio
import datetime
import re
from functools import lru_cache
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from fastapi_amis_admin import admin
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi_amis_admin.admin import ModelAdmin
from pydantic import BaseModel
from sqlalchemy import Column, Table, delete, insert
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty
from sqlalchemy.sql.elements import Label
from sqlalchemy.util import md5_hex
from sqlalchemy_database import AsyncDatabase, Database
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated, Literal

import fastapi_amis_admin
from fastapi_amis_admin.admin.handlers import register_exception_handlers
from fastapi_amis_admin.admin.parser import AmisParser
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.amis.components import (
    Action,
    ActionType,
    App,
    ColumnOperation,
    Dialog,
    Form,
    FormItem,
    Iframe,
    InputExcel,
    InputTable,
    Page,
    PageSchema,
    Picker,
    Remark,
    Service,
    TableColumn,
    TableCRUD,
    Tpl, Drawer,
)
from fastapi_amis_admin.amis.constants import DisplayModeEnum, LevelEnum, SizeEnum
from fastapi_amis_admin.amis.types import (
    AmisAPI,
    AmisNode,
    BaseAmisApiOut,
    BaseAmisModel,
    SchemaNode,
)
from fastapi_amis_admin.crud import RouterMixin, SqlalchemyCrud
from fastapi_amis_admin.crud.base import SchemaCreateT, SchemaFilterT, SchemaUpdateT, SchemaReadT
from fastapi_amis_admin.crud.parser import (
    SqlaField,
    TableModelParser,
    get_python_type_parse,
)
from fastapi_amis_admin.crud.schema import BaseApiOut, CrudEnum, Paginator
from fastapi_amis_admin.crud.utils import (
    IdStrQuery,
    SqlalchemyDatabase,
    get_engine_db,
    parser_str_set_list,
)
from fastapi_amis_admin.utils.functools import cached_property
from fastapi_amis_admin.utils.pydantic import ModelField, annotation_outer_type, create_model_by_model, deep_update, model_fields
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class SwiftAdmin(admin.ModelAdmin):

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # 启用批量新增
        self.enable_bulk_create = True
        # 启用查看
        self.schema_read = self.schema_model
        # 设置form弹出类型  Drawer | Dialog
        self.action_type = 'Drawer'


    async def get_list_table(self, request: Request) -> TableCRUD:
        '''
        headerToolbar = [
            "filter-toggler",
            "reload",
            "bulkActions",
            {"type": "columns-toggler", "align": "right"},
            {"type": "drag-toggler", "align": "right"},
            {"type": "pagination", "align": "right"},
            {
                "type": "tpl",
                "tpl": _("SHOWING ${items|count} OF ${total} RESULT(S)"),
                "className": "v-middle",
                "align": "right",
            },
        ]
        '''
        headerToolbar = [{"type": "columns-toggler", "align": "left", "draggable": False},
                         {"type": "filter-toggler", "align": "left"}]
        headerToolbar.extend(await self.get_actions(request, flag="toolbar"))
        headerToolbarright = [{"type": "export-excel", "align": "right"},
                              {"type": "reload", "align": "right"},
                              {"type": "bulkActions", "align": "right"}]
        headerToolbar.extend(headerToolbarright)
        itemActions = []
        if not self.display_item_action_as_column:
            itemActions = await self.get_actions(request, flag="item")
        filter_form = None
        if await self.has_filter_permission(request, None):
            filter_form = await self.get_list_filter_form(request)
        table = TableCRUD(
            api=await self.get_list_table_api(request),
            autoFillHeight=True,
            headerToolbar=headerToolbar,
            filterTogglable=True,
            filterDefaultVisible=False,
            filter=filter_form,
            syncLocation=False,
            keepItemSelectionOnPageChange=True,
            perPage=self.list_per_page,
            itemActions=itemActions,
            bulkActions=await self.get_actions(request, flag="bulk"),
            footerToolbar=[
                "statistics",
                "switch-per-page",
                "pagination",
                "load-more",
                {
                    "type": "tpl",
                    "tpl": _("SHOWING ${items|count} OF ${total} RESULT(S)"),
                    "className": "v-middle",
                    "align": "right",
                },
            ],
            columns=await self.get_list_columns(request),
            primaryField=self.pk_name,
            quickSaveItemApi=f"put:{self.router_path}/item/${self.pk_name}",
            defaultParams={k: v for k, v in request.query_params.items() if v},
        )
        # Append operation column
        action_columns = await self._get_list_columns_for_actions(request)
        table.columns.extend(action_columns)
        # Append inline link model column
        link_model_columns = await self._get_list_columns_for_link_model(request)
        if link_model_columns:
            table.columns.extend(link_model_columns)
            table.footable = True
        return table

    async def get_read_action(self, request: Request) -> Optional[Action]:
        if not self.schema_read:
            return None
        if self.action_type == 'Drawer':
            return ActionType.Drawer(
                icon="fas fa-eye",
                tooltip=_("View"),
                drawer=Drawer(
                    title=_("View") + " - " + _(self.page_schema.label),
                    position="right",
                    showCloseButton=False,
                    overlay=False,
                    closeOnOutside=True,
                    size=SizeEnum.lg,
                    resizable=True,
                    body=await self.get_read_form(request),
                ),
            )
        else:
            return ActionType.Dialog(
                icon="fas fa-eye",
                tooltip=_("View"),
                dialog=Dialog(
                    title=_("View") + " - " + _(self.page_schema.label),
                    position="right",
                    showCloseButton=False,
                    overlay=False,
                    closeOnOutside=True,
                    size=SizeEnum.lg,
                    resizable=True,
                    body=await self.get_read_form(request),
                ),
            )

    async def get_create_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not bulk:
            if self.action_type == 'Drawer':
                return ActionType.Drawer(
                    icon="fa fa-plus pull-left",
                    label=_("Create"),
                    level=LevelEnum.primary,
                    drawer=Drawer(
                        title=_("Create") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_create_form(request, bulk=bulk),
                    ),
                )
            else:
                return ActionType.Dialog(
                    icon="fa fa-plus pull-left",
                    label=_("Create"),
                    level=LevelEnum.primary,
                    dialog=Dialog(
                        title=_("Create") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_create_form(request, bulk=bulk),
                    ),
                )
        if self.action_type == 'Drawer':
            return ActionType.Dialog(
                icon="fa fa-plus pull-left",
                label=_("Bulk Create"),
                level=LevelEnum.primary,
                dialog=Dialog(
                    title=_("Bulk Create") + " - " + _(self.page_schema.label),
                    position="right",
                    showCloseButton=False,
                    overlay=False,
                    closeOnOutside=True,
                    size=SizeEnum.full,
                    resizable=True,
                    body=await self.get_create_form(request, bulk=bulk),
                ),
            )
        else:
            return ActionType.Dialog(
                icon="fa fa-plus pull-left",
                label=_("Bulk Create"),
                level=LevelEnum.primary,
                dialog=Dialog(
                    title=_("Bulk Create") + " - " + _(self.page_schema.label),
                    position="right",
                    showCloseButton=False,
                    overlay=False,
                    closeOnOutside=True,
                    size=SizeEnum.full,
                    resizable=True,
                    body=await self.get_create_form(request, bulk=bulk),
                ),
            )

    async def get_update_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not bulk:
            if self.action_type == 'Drawer':
                return ActionType.Drawer(
                    icon="fa fa-pencil",
                    tooltip=_("Update"),
                    drawer=Drawer(
                        title=_("Update") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_update_form(request, bulk=bulk),
                    ),
                )
            else:
                return ActionType.Dialog(
                    icon="fa fa-pencil",
                    tooltip=_("Update"),
                    dialog=Dialog(
                        title=_("Update") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_update_form(request, bulk=bulk),
                    ),
                )
        elif self.bulk_update_fields:
            if self.action_type == 'Drawer':
                return ActionType.Dialog(
                    label=_("Bulk Update"),
                    dialog=Dialog(
                        title=_("Bulk Update") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_update_form(request, bulk=True),
                    ),
                )
            else:
                return ActionType.Dialog(
                    label=_("Bulk Update"),
                    dialog=Dialog(
                        title=_("Bulk Update") + " - " + _(self.page_schema.label),
                        position="right",
                        showCloseButton=False,
                        overlay=False,
                        closeOnOutside=True,
                        size=SizeEnum.lg,
                        resizable=True,
                        body=await self.get_update_form(request, bulk=True),
                    ),
                )
        else:
            return None
