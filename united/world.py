"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import logging
from united.serverdb import SQLite3Db
from united.httpserverthread import HttpServerThread
from united.worldthread import WorldThread
from united.jsonrequesthandler import JsonRequestHandler
from united.mod.accountmod import AccountMod
from united.mod.imagedatamod import ImageDataMod
from united.mod.hyperlinkmod import HyperlinkMod

"""
世界 類別 (從 HttpServerThread 物件取得 client 傳來的 json 指令)
"""

class World:
    
    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.WARNING)
        self.accountMod = AccountMod()
        self.imageDataMod = ImageDataMod()
        self.hyperlinkMod = HyperlinkMod()
        self.dispatcherDict = {"create_player_account":self.accountMod,
                                "player_account_login":self.accountMod,
                                "get_logined_player":self.accountMod,
                                "post_image_data":self.imageDataMod,
                                "load_image_data":self.imageDataMod,
                                "create_hyperlink":self.hyperlinkMod,
                                "list_hyperlink_on_url":self.hyperlinkMod}
        self.loadWorldFromDb()
        
    #讀取
    def loadWorldFromDb(self):
        db = SQLite3Db()
        
    #儲存 
    def saveWorldToDb(self):
        db = SQLite3Db()
        
    #啟動 World
    def startWorld(self):
        JsonRequestHandler.instanceOfWorld = self #設置 world 實例物件給 handler
        self.httpserver = HttpServerThread(JsonRequestHandler)
        self.worldloop = WorldThread()
        self.httpserver.start()
        self.worldloop.start()
        
    #停止 World
    def stopWorld(self):
        self.httpserver.httpd.shutdown() #停止 serve_forever() 的 loop
        self.worldloop.shutdown() #停止 world loop
        self.httpserver.httpd.server_close() #關閉連線


