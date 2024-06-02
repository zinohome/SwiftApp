#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from datetime import date, datetime
from decimal import Decimal
from fastapi_amis_admin import models, amis
from typing import Optional, List, TYPE_CHECKING

from fastapi_amis_admin.models import Field
from sqlalchemy import func
from sqlmodel import Relationship
from sqlmodelx import SQLModel

from core import i18n as _

class SwiftSQLModel(SQLModel):
    class Config:
        use_enum_values = True
        from_attributes = True
        arbitrary_types_allowed = True

class Contractdetail(SwiftSQLModel, table=True):
    __tablename__ = 'contractdetail'
    contractdetail_id: Optional[int] = models.Field(default=None,
                                                    title='ID',
                                                    primary_key=True,
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    contract_id: Optional[int] = models.Field(default=None,
                                                    title='合同ID',
                                                    foreign_key='contract.contract_id',
                                                    nullable=False,
                                                    index=True,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    item_number: str = models.Field(default=None,
                                                    title='品号',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    item_name: str = models.Field(default=None,
                                                    title='名称',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    item_spec: str = models.Field(default=None,
                                                    title='规格',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    item_quantity: int = models.Field(default=None,
                                                    title='数量',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    unit_price: Decimal = models.Field(default=None,
                                                    title='单价',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    item_mount: Decimal = models.Field(default=None,
                                                    title='金额',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    create_time: datetime = models.Field(default_factory= datetime.now,
                                                    title='Create Time',
                                                    nullable=False,
                                                    index=True,
                                                    amis_form_item=amis.InputDatetime(disabled=True),
                                                    amis_table_column = "")
    update_time: Optional[datetime] = models.Field(default_factory= datetime.now,
                                                    title='Update Time',
                                                    nullable=False,
                                                    index=True,
                                                    sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
                                                    amis_form_item=amis.InputDatetime(disabled=True),
                                                    amis_table_column = "")
