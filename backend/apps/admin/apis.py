#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp

from fastapi import APIRouter
from fastapi_amis_admin.globals.deps import AsyncSess, SyncSess

router = APIRouter()


@router.get('/hello')
async def hello(name: str = '') -> str:
    return f'hello {name}'


@router.get("/test_sync_db", summary="测试同步数据库操作")
def test_sync_db(sess: SyncSess):
    # obj=sess.get(...)
    # do something
    pass


@router.get("/test_async_db", summary="测试异步数据库操作")
async def test_async_db(sess: AsyncSess):
    # obj=await sess.get(...)
    # do something
    pass

# from fastapi_user_authuser_auth.globals.deps import CurrentUser
#
# @router.get("/get_user", summary="获取当前登录用户")
# async def get_user(user: CurrentUser):
#     return user