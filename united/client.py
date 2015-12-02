"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from http.client import HTTPConnection
from united.message import Message
import json
import urllib.parse
"""
使用者端主程式
"""
class Client:

    #構構子
    def __init__(self):
        self.conn = HTTPConnection("127.0.0.1", 8000)

    #對 server 送出訊息
    def sendMessage(self, message):
        headers = {"Content-type":"application/json; charset=utf-8",
                   "Accept":"application/json; charset=utf-8",
                   "Accept-Charset":"UTF-8"}
        body = message.encoding_to_json()
        self.conn.request("POST", "/", body, headers)
        res = self.conn.getresponse()
        res_raw = res.read()
        res_data = res_raw.decode("utf-8")
        res_message = Message(None, None).decoding_from_json(res_data)
        return res_message

    #關閉 server 連線
    def closeConnection(self):
        self.conn.close()
