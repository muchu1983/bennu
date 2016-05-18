# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license
<https://opensource.org/licenses/BSD-3-Clause>
"""
import sqlite3
import os
import logging
from pymongo import MongoClient
from bennu.filesystemutility import FileSystemUtility
"""
外部資料庫存取
"""
#外部資料庫 cameo 210.65.11.231
class CameoMongoDb:
    
    #建構子
    def __init__(self):
        logging.info("connect to cameo 210.65.11.231 mongo db.")
        self.client = MongoClient("mongodb://210.65.11.231:27017/")
        
    #解構子
    def __del__(self):
        logging.info("close cameo 210.65.11.231 mongo db connection.")
        self.client.close() #關閉資料庫連線
        
    #取得 mongodb client
    def getClient(self):
        return self.client
        