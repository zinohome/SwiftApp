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

from pysondb import PysonDB
from fastapi import FastAPI
from appdef.appdef import Appdef
from starlette_exporter import PrometheusMiddleware, handle_metrics
from jaeger_client import Config as jaeger_config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing_instrumentation.client_hooks import install_all_patches
from starlette_opentracing import StarletteTracingMiddleWare
from utils.log import log as log

appdef = Appdef()

# API prefix
apiprefix = appdef.Def.Config.API_Prefix
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

# jaeger_tracer
opentracing_config = jaeger_config(
    config={
        "sampler": {"type": "const", "param": 1},
        "logging": True,
        "local_agent": {"reporting_host": appdef.Def.Config.jaeger_host},
    },
    scope_manager=ContextVarsScopeManager(),
    service_name="SwiftBuilder-" + appdef.Def.AppName,
)
jaeger_tracer = opentracing_config.initialize_tracer()
install_all_patches()
app.add_middleware(StarletteTracingMiddleWare, tracer=jaeger_tracer)

