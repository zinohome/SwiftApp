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

from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.staticfiles import StaticFiles
from core.adminsite import site
from appdef.appdef import Appdef
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette.responses import RedirectResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from utils.log import log as log

appdef = Appdef()

# API prefix
apiprefix = appdef.Def.Config.api_prefix
if apiprefix is not None:
    if apiprefix.startswith('/'):
        pass
    else:
        apiprefix = '/' + apiprefix
else:
    apiprefix = '/swiftapp'
app = FastAPI(debug=appdef.Def.Config.debug,
              title=appdef.Def.AppName,
              description=appdef.Def.Description,
              version=appdef.Def.Version,
              openapi_url=apiprefix + "/openapi.json",
              docs_url=None,
              redoc_url=None
              )
# starlette_exporter
app.add_middleware(
    PrometheusMiddleware,
    app_name=appdef.Def.AppName,
    prefix=apiprefix[1:],
    labels={
        "server_name": os.getenv("HOSTNAME"),
    },
    group_paths=True,
    buckets=[0.1, 0.25, 0.5],
    skip_paths=['/health'],
    always_use_int_status=False)
app.add_route("/metrics", handle_metrics)

# setup app
#from apps import admin
#admin.setup(app)

# mount admin app
site.mount_app(app)

@app.on_event("startup")
async def startup():
    from core.adminsite import auth
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    # Create a default test user, please change the password in time!!!
    await auth.create_role_user('admin')
    await auth.create_role_user('vip')

@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)

# 1.配置 CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=appdef.Def.Config.allow_origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)
# 2. 配置静态资源目录
app.mount("/static", StaticFiles(directory="apps/static"), name="static")

# 3.配置 Swagger UI CDN
from fastapi.openapi.docs import get_swagger_ui_html
@app.get("/apidocs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{appdef.Def.AppName} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_favicon_url="/static/favicon.ico",
        swagger_css_url="/static/swagger-ui-dist@4/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# 4.配置 Redoc CDN
@app.get("/apiredoc", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{appdef.Def.AppName} - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico",
        with_google_fonts=False,
    )