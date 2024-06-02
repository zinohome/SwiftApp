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

class Contract(SwiftSQLModel, table=True):
    __tablename__ = 'contract'
    contract_id: Optional[int] = models.Field(default=None,
                                                    title='ID',
                                                    primary_key=True,
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    contact_number: str = models.Field(default=None,
                                                    title='合同编号',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    contact_type: str = models.Field(default=None,
                                                    title='合同类型',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    sign_date: date = models.Field(default=None,
                                                    title='签约时间',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    sign_address: str = models.Field(default=None,
                                                    title='签约地点',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    customer_name: str = models.Field(default=None,
                                                    title='甲方',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    supplier_name: str = models.Field(default=None,
                                                    title='乙方',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    quality_standard: str = models.Field(default=None,
                                                    title='质量标准',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    delivery_data: str = models.Field(default=None,
                                                    title='交货期',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    package_requirements: str = models.Field(default=None,
                                                    title='包装要求',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    delivery_address: str = models.Field(default=None,
                                                    title='交货地点',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    other_agreements: str = models.Field(default=None,
                                                    title='其它约定事项',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    back_terms: str = models.Field(default=None,
                                                    title='背面条款',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    dispute_settlements: str = models.Field(default=None,
                                                    title='争议解决办法',
                                                    nullable=False,
                                                    index=False,
                                                    amis_form_item = "",
                                                    amis_table_column = "")
    contract_amount: Decimal = models.Field(default=None,
                                                    title='合同金额',
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
