#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from apps.admin.models.contracts import Contracts
from core.globals import site
from typing import List, Optional
from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema, TableColumn, ActionType, Action, Dialog, SizeEnum, Drawer, LevelEnum, \
    TableCRUD
from starlette.requests import Request
import simplejson as json
from fastapi_amis_admin.utils.translation import i18n as _

class ContractAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Contracts', page_title='Contracts', icon='fa fa-border-all')
    model = Contracts
    pk_name = 'contract_id'

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
    async def get_read_action(self, request: Request) -> Optional[Action]:
        if not self.schema_read:
            return None
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

    async def get_create_action(self, request: Request, bulk: bool = False) -> Optional[Action]:
        if not bulk:
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
        return ActionType.Drawer(
            icon="fa fa-plus pull-left",
            label=_("Bulk Create"),
            level=LevelEnum.primary,
            drawer=Drawer(
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
        elif self.bulk_update_fields:
            return ActionType.Drawer(
                label=_("Bulk Update"),
                drawer=Drawer(
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