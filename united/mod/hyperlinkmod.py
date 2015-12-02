"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""

import base64
import uuid
from united.message import Message
from united.lockedcase import LockedCase
from united.serverdb import SQLite3Db

"""
圖塊超連結 模組
"""
class HyperlinkMod:

    #構構子
    def __init__(self):
        pass
        
    def dispatchMessage(self, message):
        message_title = message.getTitle()
        res_message = None
        if message_title == "create_hyperlink":
            res_message = self.createHyperlink(message)
        elif message_title == "list_hyperlink_on_url":
            res_message = self.listHyperlinkOnUrl(message)
        return res_message
        
    #在 索引表 中 建立超連結
    def createHyperlink(self, message):
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "create_hyperlink"
            contents = {"hyperlink":"test",
                        "url":"root",
                        "json_coords":"[10,20,110,80]",
                        "shape":"rectangle",
                        "description":"XXXXXXXXXXXXX"}
            回傳的 message 格式
            title = "create_hyperlink"
            contents = {"status":0}
        """
        db = SQLite3Db()
        db.insertOne("indextable", [None,
                                    message.getContents()["hyperlink"],
                                    message.getContents()["url"],
                                    message.getContents()["json_coords"],
                                    message.getContents()["shape"],
                                    message.getContents()["description"]])
        ret_m = Message("create_hyperlink", {"status":0})
        return ret_m
    
    #列出 url 下的所有超連結
    def listHyperlinkOnUrl(self, message):
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "list_hyperlink_on_url"
            contents = {"url":"aaaaa"}
            回傳的 message 格式
            title = "list_hyperlink_on_url"
            contents = {"status":0,
                        "hyperlink_list":[["hyperlink","json_coords","shape","description"],[...],...]}
        """
        db = SQLite3Db()
        hl_list = db.selectSpecify("indextable", {"url":message.getContents()["url"]})
        hyperlink_data_list = []
        for hl in hl_list:
            hl_data = [hl[1], hl[3], hl[4], hl[5]]
            hyperlink_data_list.append(hl_data)
        ret_m = Message("list_hyperlink_on_url", {"status":0, "hyperlink_list":hyperlink_data_list})
        return ret_m
        