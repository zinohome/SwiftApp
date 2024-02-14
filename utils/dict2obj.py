#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

import os
from functools import singledispatch
from types import SimpleNamespace

@singledispatch
def dict2obj(o):
    return o

@dict2obj.register(dict)
def handle_obj(obj):
    return SimpleNamespace(**{k: dict2obj(v) for k, v in obj.items()})

@dict2obj.register(list)
def handle_list(lst):
    return [dict2obj(i) for i in lst]
