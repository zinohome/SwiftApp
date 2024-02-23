#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
import importlib
import traceback
import re
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Pattern,
    Tuple,
    Type,
    Union,
)
from fastapi_amis_admin import admin, amis
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi_amis_admin.admin import AdminAction
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
from fastapi_amis_admin.crud import BaseApiOut, ItemListSchema
from fastapi_amis_admin.crud.base import SchemaCreateT, SchemaUpdateT
from fastapi_amis_admin.crud.parser import parse_obj_to_schema, TableModelT
from fastapi_user_auth.mixins.admin import AuthFieldModelAdmin, AuthSelectModelAdmin
from sqlalchemy import func, Select
from typing_extensions import Annotated, Literal
from fastapi_amis_admin.utils.translation import i18n as _
from utils.log import log as log

class SwiftAdmin(AuthSelectModelAdmin):

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # 启用批量新增
        self.enable_bulk_create = False
        # 启用查看
        self.schema_read = self.schema_model
        # 设置form弹出类型  Drawer | Dialog
        self.action_type = 'Drawer'
        # 设置item action
        self.display_item_action_as_column = False
        self.bind_model = True

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list

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

    async def get_sub_list_table(self, subobj: "SwiftAdmin", request: Request) -> TableCRUD:
        try:
            subobj.enable_bulk_create = False
            #subobj.register_crud()
            subobj.display_item_action_as_column = False
            headerToolbar = [{"type": "columns-toggler", "align": "left", "draggable": False}]
            headerToolbar.extend(await subobj.get_actions(request, flag="toolbar"))
            headerToolbarright = [{"type": "reload", "align": "right"},
                              {"type": "bulkActions", "align": "right"}]
            headerToolbar.extend(headerToolbarright)
            itemActions = []
            if not subobj.display_item_action_as_column:
                itemActions = await subobj.get_actions(request, flag="item")
            table = TableCRUD(
                api=await subobj.get_list_table_api(request),
                autoFillHeight=True,
                headerToolbar=headerToolbar,
                filterTogglable=False,
                filterDefaultVisible=False,
                syncLocation=False,
                keepItemSelectionOnPageChange=True,
                perPage=subobj.list_per_page,
                itemActions=itemActions,
                bulkActions=await subobj.get_actions(request, flag="bulk"),
                footable=True,
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
                columns=await subobj.get_list_columns(request),
                primaryField=subobj.pk_name,
                quickSaveItemApi=f"put:{subobj.router_path}/item/${subobj.pk_name}",
                defaultParams={k: v for k, v in request.query_params.items() if v},
            )
            # Append operation column
            action_columns = await subobj._get_list_columns_for_actions(request)
            table.columns.extend(action_columns)
            # Append inline link model column
            link_model_columns = await subobj._get_list_columns_for_link_model(request)
            if link_model_columns:
                table.columns.extend(link_model_columns)
                table.footable = True
            return table
        except Exception as exp:
            print('Exception at SwiftAdmin.get_sub_list_table() %s ' % exp)
            traceback.print_exc()

    async def get_read_form(self, request: Request) -> Form:
        r_form = await super().get_read_form(request)
        return r_form

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request, bulk)
        return u_form

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

    @property
    def route_list(self) -> Callable:
        async def route(
            request: Request,
            sel: self.AnnotatedSelect,  # type: ignore
            paginator: Annotated[self.paginator, Depends()],  # type: ignore
            filters: Annotated[self.schema_filter, Body()] = None,  # type: ignore
        ):
            if not await self.has_list_permission(request, paginator, filters):
                return self.error_no_router_permission(request)
            data = ItemListSchema(items=[])
            data.query = request.query_params
            if await self.has_filter_permission(request, filters):
                data.filters = await self.on_filter_pre(request, filters)
                if data.filters:
                    sel = sel.filter(*self.calc_filter_clause(data.filters))
            if paginator.showTotal:
                data.total = await self.db.async_scalar(sel.with_only_columns(func.count("*")))
                if data.total == 0:
                    return BaseApiOut(data=data)
            orderBy = self._calc_ordering(paginator.orderBy, paginator.orderDir)
            if orderBy:
                sel = sel.order_by(*orderBy)
            sel = sel.limit(paginator.perPage).offset(paginator.offset)
            result = await self.db.async_execute(sel)
            return BaseApiOut(data=await self.on_list_after(request, result, data))

        return route

    @property
    def route_create(self) -> Callable:
        async def route(
            request: Request,
            data: Annotated[Union[List[self.schema_create], self.schema_create], Body()],  # type: ignore
        ) -> BaseApiOut[Union[int, self.schema_model]]:  # type: ignore
            if not await self.has_create_permission(request, data):
                return self.error_no_router_permission(request)
            if not isinstance(data, list):
                data = [data]
            try:
                items = await self.create_items(request, data)
            except Exception as error:
                await self.db.async_rollback()
                return self.error_execute_sql(request=request, error=error)
            result = len(items)
            if result == 1:  # if only one item, return the first item
                result = await self.db.async_run_sync(lambda _: parse_obj_to_schema(items[0], self.schema_model, refresh=True))
            return BaseApiOut(data=result)

        return route

    @property
    def route_read(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
        ):
            if not await self.has_read_permission(request, item_id):
                return self.error_no_router_permission(request)
            items = await self.read_items(request, item_id)
            return BaseApiOut(data=items if len(items) > 1 else items[0])

        return route

    @property
    def route_update(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
            data: Annotated[self.schema_update, Body()],  # type: ignore
        ):
            if not await self.has_update_permission(request, item_id, data):
                return self.error_no_router_permission(request)
            values = await self.on_update_pre(request, data, item_id=item_id)
            if not values:
                return self.error_data_handle(request)
            items = await self.update_items(request, item_id, values)
            return BaseApiOut(data=len(items))

        return route

    @property
    def route_delete(self) -> Callable:
        async def route(
            request: Request,
            item_id: self.AnnotatedItemIdList,  # type: ignore
        ):
            if not await self.has_delete_permission(request, item_id):
                return self.error_no_router_permission(request)
            items = await self.delete_items(request, item_id)
            return BaseApiOut(data=len(items))

        return route

    async def on_create_pre(self, request: Request, obj: SchemaCreateT, **kwargs) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj)
        return data

    async def on_update_pre(
            self,
            request: Request,
            obj: SchemaUpdateT,
            item_id: Union[List[str], List[int]],
            **kwargs,
    ) -> Dict[str, Any]:
        data = await super().on_update_pre(request, obj, item_id)
        return data

    async def update_items(self, request: Request, item_id: List[str], values: Dict[str, Any]) -> List[TableModelT]:
        return await super().update_items(request, item_id, values)