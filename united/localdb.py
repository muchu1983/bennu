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
資料庫存取 類別
"""

class SQLite3Db:

    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        dbPath = os.getcwd() + "\\resource\\local.db"
        if os.path.exists(dbPath):
            logging.info("connect to sqlite3 db.")
            self.conn = sqlite3.connect(dbPath)
        else: #初始化 db
            logging.info("connect to sqlite3 db with initialization.")
            self.conn = sqlite3.connect(dbPath)
            c = self.conn.cursor()
            c.execute("""CREATE TABLE table
                            (id INTEGER PRIMARY KEY)""")
            self.conn.commit()

    #解構子
    def __del__(self):
        logging.info("close sqlite3 db connection.")
        self.conn.close() #關閉資料庫

    # insert 一筆資料
    def insertOne(self, table, data):
        c = self.conn.cursor()
        data_str = []
        for d in data:
            if type(d) == str:
                data_str.append("'" + d + "'")
            elif d == None:
                data_str.append("null")
            else:
                data_str.append(str(d))
        data_str = ",".join(data_str)
        sql = "INSERT INTO " + table + " VALUES(" + data_str + ")"
        c.execute(sql)
        self.conn.commit()

    # select 全部資料
    def selectAll(self, table):
        c = self.conn.cursor()
        sql = "SELECT * FROM " + table
        c.execute(sql)
        return c.fetchall()
