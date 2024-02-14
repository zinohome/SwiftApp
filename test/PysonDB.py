#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

from pysondb import PysonDB
from utils.log import log as log
import simplejson as json


#db = PysonDB('../appdef/app.json')

if __name__ == '__main__':
    log.debug(json.load(open('../appdef/app.json')))