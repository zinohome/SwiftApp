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
from loguru import logger as log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'log')
LOG_PATH = os.path.join(LOG_DIR, 'SwiftApp.log')
log.add(LOG_PATH,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="100 MB",
            retention="14 days",
            level="DEBUG",
            enqueue=True)

if __name__ == '__main__':
    log.success('[测试log] hello, world')
    log.info('[测试log] hello, world')
    log.debug('[测试log] hello, world')
    log.trace('[测试log] hello, world')
    log.warning('[测试log] hello, world')
    log.error('[测试log] hello, world')
    log.critical('[测试log] hello, world')