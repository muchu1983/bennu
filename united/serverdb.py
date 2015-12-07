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
資料庫存取 類別 (Server)
"""

class SQLite3Db:

    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        dbPath = os.getcwd() + "/united_res/server.db"
        if os.path.exists(dbPath):
            logging.info("connect to sqlite3 db.(server.db)")
            self.conn = sqlite3.connect(dbPath)
        else: #初始化 db
            logging.info("connect to sqlite3 db with initialization.(server.db)")
            self.conn = sqlite3.connect(dbPath)
            c = self.conn.cursor()
            #玩家表
            c.execute("""CREATE TABLE player
                            (id INTEGER PRIMARY KEY,
                            account TEXT,
                            hashed BLOB,
                            playerUUID TEXT,
                            playerName TEXT,
                            playerPrestige INTEGER)""")
            c.execute("""CREATE TABLE indextable
                            (id INTEGER PRIMARY KEY,
                            hyperlink TEXT,
                            masterurl TEXT,
                            coords TEXT,
                            shape TEXT,
                            description TEXT)""")
            c.execute("""CREATE TABLE image
                            (id INTEGER PRIMARY KEY,
                            url TEXT,
                            data BLOB,
                            mode TEXT,
                            width INTEGER,
                            height INTEGER)""")
            self.conn.commit()
            
    #解構子
    def __del__(self):
        logging.info("close sqlite3 db connection.(server.db)")
        self.conn.close() #關閉資料庫
    
    #insert 玩家資料 (含有 hashed blob 資料型態)
    def insertOnePlayer(self, data):
        c = self.conn.cursor()
        account = data[0]
        hashed = data[1]
        playerUUID = data[2]
        playerName = data[3]
        sql = "INSERT INTO player VALUES(null, '" + account + "', ?, '" + playerUUID + "', '" + playerName + "', 0)"
        c.execute(sql, [sqlite3.Binary(hashed)])
        self.conn.commit()
    
    # 使用 account select 一筆玩家資料 (含有 hashed blob 資料型態)
    def selectOnePlayer(self, account):
        c = self.conn.cursor()
        sql = "SELECT * FROM player WHERE account = '" + account + "'"
        c.execute(sql)
        return c.fetchone()
        
    # 使用 UUID select 一筆玩家資料 (含有 hashed blob 資料型態)
    def selectUUIDPlayer(self, player_uuid):
        c = self.conn.cursor()
        sql = "SELECT * FROM player WHERE playerUUID = '" + player_uuid + "'"
        c.execute(sql)
        return c.fetchone()

    # insert 一筆資料
    def insertOne(self, table, data):
        c = self.conn.cursor()
        blob_data = []
        data_str = []
        for d in data:
            if type(d) == str:
                data_str.append("'" + d + "'")
            elif type(d) == bytes:
                data_str.append("?")
                blob_data.append(sqlite3.Binary(d))
            elif d == None:
                data_str.append("null")
            else:
                data_str.append(str(d))
        data_str = ",".join(data_str)
        sql = "INSERT INTO " + table + " VALUES(" + data_str + ")"
        c.execute(sql, blob_data)
        self.conn.commit()

    # select 全部資料
    def selectAll(self, table):
        c = self.conn.cursor()
        sql = "SELECT * FROM " + table
        c.execute(sql)
        return c.fetchall()
        
    # select 指定資料
    def selectSpecify(self, table, where_dict):
        c = self.conn.cursor()
        where_len = len(where_dict.keys())
        current = 0
        where_sql = ""
        for key in where_dict.keys():
            target_value = where_dict[key]
            if type(target_value) == str: target_value = "'" + target_value + "'" #字串型態加上引號
            elif target_value == None: target_value = "null" # None = null
            else: target_value = str(target_value)
            where_sql = where_sql + key + " = " + target_value
            current += 1
            if current < where_len:
                where_sql += " AND "
        sql = "SELECT * FROM " + table + " WHERE " + where_sql
        c.execute(sql)
        return c.fetchall()
        
    #清除 table 內所有資料
    def clearTable(self, table):
        c = self.conn.cursor()
        sql = "DELETE FROM " + table
        c.execute(sql)
        self.conn.commit()
        
    #刪除 指定資料
    def deleteSpecify(self, table, where_dict):
        c = self.conn.cursor()
        where_len = len(where_dict.keys())
        current = 0
        where_sql = ""
        for key in where_dict.keys():
            target_value = where_dict[key]
            if type(target_value) == str: target_value = "'" + target_value + "'" #字串型態加上引號
            elif target_value == None: target_value = "null" # None = null
            else: target_value = str(target_value)
            where_sql = where_sql + key + " = " + target_value
            current += 1
            if current < where_len:
                where_sql += " AND "
        sql = "DELETE FROM " + table + " WHERE " + where_sql
        c.execute(sql)
        self.conn.commit()
    
    # update 指定資料
    def updateSpecify(self, table, set_dict, where_dict):
        c = self.conn.cursor()
        set_len = len(set_dict.keys())
        curr_set = 0
        set_sql = ""
        for key in set_dict.keys():
            target_value = set_dict[key]
            if type(target_value) == str: target_value = "'" + target_value + "'" #字串型態加上引號
            elif target_value == None: target_value = "null" # None = null
            else: target_value = str(target_value)
            set_sql = set_sql + key + " = " + target_value
            curr_set += 1
            if curr_set < set_len:
                set_sql += " , "
        # 這是分隔線
        where_len = len(where_dict.keys())
        curr_where = 0
        where_sql = ""
        for key in where_dict.keys():
            target_value = where_dict[key]
            if type(target_value) == str: target_value = "'" + target_value + "'" #字串型態加上引號
            elif target_value == None: target_value = "null" # None = null
            else: target_value = str(target_value)
            where_sql = where_sql + key + " = " + target_value
            curr_where += 1
            if curr_where < where_len:
                where_sql += " AND "
        sql = "UPDATE " + table +" SET " + set_sql + " WHERE " + where_sql
        c.execute(sql)
        self.conn.commit()
        