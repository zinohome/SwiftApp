#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from sqlmodel import SQLModel

from core.globals import site, auth
from core.settings import settings
from utils.log import log as log

app = FastAPI(debug=settings.debug)
# 在app应用下每条请求处理之前都附加`request.auth`和`request.user`对象
auth.backend.attach_middleware(app)

# 安装应用
from apps import admin
admin.setup(app.router, site)

# 挂载后台管理系统
site.mount_app(app)

# 注意1: site.mount_app会默认添加site.db的session会话上下文中间件,如果你使用了其他的数据库连接,请自行添加.例如:
# from core.globals import sync_db
# app.add_middleware(sync_db.asgi_middleware) # 注意中间件的注册顺序.

# 注意2: 非请求上下文中,请自行创建session会话,例如:定时任务,测试脚本等.
# from core.globals import async_db
# async with async_db():
#     async_db.async_get(...)
#     async_db.session.get(...)
#     # do something


@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    # 创建默认管理员,用户名: admin,密码: admin, 请及时修改密码!!!
    await auth.create_role_user("admin")
    # 创建默认超级管理员,用户名: root,密码: root, 请及时修改密码!!!
    await auth.create_role_user("root")
    # 运行site的startup方法,加载casbin策略等
    await site.router.startup()
    if not auth.enforcer.enforce("u:admin", site.unique_id, "page", "page"):
        await auth.enforcer.add_policy("u:admin", site.unique_id, "page", "page", "allow")


@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)

# 要求: 用户必须登录
@app.get("/auth/get_user")
@auth.requires()
def get_user(request: Request):
    return request.user