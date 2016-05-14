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
本機端資料庫存取
"""
class SQLite3Db:

    #建構子
    def __init__(self, strResFolderPath=None):
        logging.basicConfig(level=logging.INFO)
        self.fsUtil = FileSystemUtility()
        strDbPath = self.fsUtil.getPackageResourcePath(strPackageName=strResFolderPath, strResourceName="local.db")
        logging.info("connect to sqlite3 db.")
        self.conn = sqlite3.connect(strDbPath) #建立連線
        self.conn.row_factory = sqlite3.Row #資料封裝為 Row 物件
            
    #解構子
    def __del__(self):
        logging.info("close sqlite3 db connection.")
        self.conn.close() #關閉資料庫連線
        
    # 執行 SQL 並 commit (適用於 INSERT、UPDATE、DELETE)
    def commitSQL(self, strSQL=None):
        c = self.conn.cursor()
        c.execute(strSQL)
        self.conn.commit()
        return c.lastrowid #回傳最後 INSERT 的 row id

    # 執行 SQL 並 fetchall 資料 (適用於 SELECT)
    def fetchallSQL(self, strSQL=None):
        c = self.conn.cursor()
        c.execute(strSQL)
        return c.fetchall()
        
class MongoDb:
    
    #建構子
    def __init__(self):
        logging.info("connect to mongo db.")
        self.client = MongoClient("mongodb://localhost:27017/")
        
    #解構子
    def __del__(self):
        logging.info("close mongo db connection.")
        self.client.close() #關閉資料庫連線
        
    #取得 mongodb client
    def getClient(self):
        return self.client
        
#匯率API
class LocalDbForCurrencyApi:
    
    #建構子
    def __init__(self):
        self.mongodb = MongoDb().getClient().localdb