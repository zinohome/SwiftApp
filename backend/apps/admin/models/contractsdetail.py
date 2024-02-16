#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from datetime import date
from decimal import Decimal

from fastapi_amis_admin import models
from typing import Optional, TYPE_CHECKING

from sqlmodel import Relationship
from sqlmodelx import SQLModel
from core import i18n as _

if TYPE_CHECKING:
    import Contracts

class SwiftSQLModel(SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True

class Contractsdetail(SwiftSQLModel, table=True):
    __tablename__ = 'contractsdetail'
    contractdetail_id: Optional[int] = models.Field(default=None, title='ID', primary_key=True, amis_form_item='',
                                              amis_table_column='')
    contract_id: Optional[int] = models.Field(default=None, title='合同ID', primary_key=False, amis_form_item='',
                                              amis_table_column='')
    item_number: str = models.Field(default=None, title='品号', nullable=False, amis_form_item='',
                                       amis_table_column='')
    item_name: str = models.Field(default=None, title='名称', nullable=False, amis_form_item='',
                                       amis_table_column='')
    item_spec: date = models.Field(default=None, title='规格', nullable=False, amis_form_item='',
                                   amis_table_column='')
    item_quantity: int = models.Field(default=None, title='数量', nullable=False, amis_form_item='',
                                   amis_table_column='')
    unit_price: Decimal = models.Field(default=None, title='单价', nullable=False, amis_form_item='',
                                      amis_table_column='')
    item_mount: Decimal = models.Field(default=None, title='金额', nullable=False, amis_form_item='',
                                      amis_table_column='')
    cdcontact: "Contracts" = Relationship(back_populates="cddtails")
