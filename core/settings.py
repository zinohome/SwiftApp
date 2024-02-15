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
from pathlib import Path
from typing import List
from fastapi_amis_admin.admin.settings import Settings as AmisSettings
from appdef.appdef import Appdef

appdef = Appdef()
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(AmisSettings):
    name: str = appdef.Def.AppName
    host: str = '0.0.0.0'
    port: int = int(appdef.Def.Config.listenport)
    debug: bool = appdef.Def.Config.debug
    secret_key: str = 'veheyyw6pv1nqtjsdbgt56yhn0hbhjltn42k7nlaikl4rn62bwewawq0qt9o6723'
    version: str = appdef.Def.Version
    site_title: str = appdef.Def.AppName
    site_icon: str = '/static/favicon.ico'
    language: str = appdef.Def.Config.language
    amis_cdn: str = '/static/'
    amis_theme: str = appdef.Def.Config.amis_theme
    allow_origins: List[str] = appdef.Def.Config.allow_origins.split(",")
    language: str = appdef.Def.Config.language
    database_url_async: str = appdef.Def.Config.database_url_async


#settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))
settings = Settings()
settings.database_url_async = appdef.Def.Config.database_url_async

if __name__ == '__main__':
    print(settings)
    print(settings.database_url_async)
    print(settings.allow_origins)