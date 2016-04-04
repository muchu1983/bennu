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
"""
本機端資料庫存取
"""
class SQLite3Db:

    #建構子
    def __init__(self, strResFolderPath=None):
        logging.basicConfig(level=logging.INFO)
        dbPath = os.sep.join([strResFolderPath, "local.db"])
        logging.info("connect to sqlite3 db.")
        self.conn = sqlite3.connect(dbPath) #建立連線
            
    #解構子
    def __del__(self):
        logging.info("close sqlite3 db connection.")
        self.conn.close() #關閉資料庫連線
        
    # 執行 SQL 並 commit (適用於 INSERT、UPDATE、DELETE)
    def commitSQL(self, strSQL=None):
        c = self.conn.cursor()
        c.execute(strSQL)
        self.conn.commit()

    # 執行 SQL 並 fetchall 資料 (適用於 SELECT)
    def fetchallSQL(self, strSQL=None):
        c = self.conn.cursor()
        c.execute(strSQL)
        return c.fetchall()