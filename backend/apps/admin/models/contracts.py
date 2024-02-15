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
from typing import Optional
import sqlmodel

class BaseSQLModel(sqlmodel.SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True

class Contracts(BaseSQLModel, table=True):
    __tablename__ = 'contracts'
    contract_id: Optional[int] = models.Field(default=None, title='contract_id', primary_key=True, amis_form_item='', amis_table_column='')
    customer_name: str = models.Field(default=None, title='customer_name', nullable=False, amis_form_item='', amis_table_column='')
    contract_amount: Decimal = models.Field(default=None, title='contract_amount', nullable=False, amis_form_item='', amis_table_column='')
    sign_date: date = models.Field(default=None, title='sign_date', nullable=False, amis_form_item='', amis_table_column='')