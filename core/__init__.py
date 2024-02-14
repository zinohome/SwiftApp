#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2023 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2023
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: SwiftApp
import gettext
import os

from appdef.appdef import Appdef
from utils.translation import i18n

appdef = Appdef()
applan = appdef.Def.Config.language
i18n.set_language(applan)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_translations({
    applan: gettext.translation(
        domain='messages',
        localedir=os.path.join(BASE_DIR, "locale"),
        languages=[applan]
    )
})