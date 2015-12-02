"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import logging
from united.region import Region
from united.serverdb import SQLite3Db
from united.httpserverthread import HttpServerThread
from united.jsonrequesthandler import JsonRequestHandler

"""
世界 類別 (從 HttpServerThread 物件取得 client 傳來的 json 指令)
"""

class World:
    
    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.WARNING)
        #預設區域
        r0 = Region("sandbox") # 測試用 
        r0.addRole("muchu", 100, 100)
        r0.addRole("luna", 300, 300)
        r1 = Region("台北市")
        r2 = Region("台中市")
        r3 = Region("台南市")
        r4 = Region("高雄市")
        r5 = Region("宜蘭縣")
        r6 = Region("花蓮縣")
        r7 = Region("台東縣")
        r8 = Region("澎湖縣")
        self.region = [r0, r1, r2, r3, r4, r5, r6, r7, r8]
        self.loadWorldFromDb()
        
    #讀取
    def loadWorldFromDb(self):
        db = SQLite3Db()
        #role data
        for re in self.region:
            role_list = db.selectSpecify("role", {"regionName":re.name})
            for role_data in role_list:
                re.addRole(role_data[1], role_data[2], role_data[3])
        #dream id data
        for re in self.region:
            region_name = re.name
            for ro in re.role:
                role_name = ro.name
                dream_list = db.selectSpecify("dream", {"region_name":region_name, "role_name":role_name})
                for dream_data in dream_list:
                    ro.dreamIdList.append(dream_data[0])
        
    #儲存 (sandbox region 的資料不會被 saveWorldToDb 存入)
    def saveWorldToDb(self):
        db = SQLite3Db()
        db.clearTable("role")
        for re in self.region:
            region_name = re.name
            if region_name != "sandbox":
                for ro in re.role:
                    db.insertOne("role", [None, ro.name, ro.region_x, ro.region_y, region_name])
        

    #啟動 HTTP server
    def startHTTPServer(self):
        JsonRequestHandler.instanceOfWorld_read_only = self #設置 world 實例物件給 handler
        self.httpserver = HttpServerThread(JsonRequestHandler)
        self.httpserver.start()
        
    #停止 HTTP server
    def stopHTTPServer(self):
        self.httpserver.httpd.shutdown() #停止 serve_forever() 的 loop
        self.httpserver.httpd.server_close() #關閉連線


