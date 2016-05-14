# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import pkg_resources
import sys
class FileSystemUtility:
    
    #取得 package 資源路徑
    def getPackageResourcePath(self, strPackageName=None, strResourceName=None):
        strRawResPath = pkg_resources.resource_filename(strPackageName, strResourceName)
        strUnicodeResPath = None
        if sys.version_info[0] == 2: #python 2 路徑編碼為系統編碼，需轉為 unicode 物件
            strUnicodeResPath = strRawResPath.decode(sys.getfilesystemencoding())
        if sys.version_info[0] == 3: #python 3 已經是 unicode 物件，不需轉換
            strUnicodeResPath = strRawResPath
        return strUnicodeResPath
        