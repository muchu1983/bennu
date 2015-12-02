"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import logging
import base64
import uuid
from http.server import BaseHTTPRequestHandler
from united.message import Message
from united.lockedcase import LockedCase
"""
自定義 HTTP Request handler
"""

class JsonRequestHandler(BaseHTTPRequestHandler):
    #從world 讀取資訊再回覆給 client (唯讀用法)
    instanceOfWorld_read_only = None # class 靜態變數,server 啟動前設置為 world 實例物件
    # do_Get 測試用
    def do_GET(self):
        print("someone get in!")
        self.send_response(400) #狀態碼 400
    
    #覆寫 do_POST
    def do_POST(self):
        post_raw = self.rfile.read(int(self.headers.get("Content-Length"))) #bytes
        post_data = post_raw.decode("utf-8") # bytes to str
        post_message = Message(None, None).decoding_from_json(post_data)
        message_title = post_message.getTitle()
        if message_title == "just_for_test":
            #僅供測試使用
            ans_message = self.justfortest(post_message)
            self.sendResponseJsonMessage(200, ans_message) #狀態碼 200 -> 成功
        elif message_title == "create_player_account":
            #建立新的玩家帳號
            res_message = self.createPlayerAccount(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "player_account_login":
            #帳號登入取得UUID
            res_message = self.playerAccountLogin(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "get_logined_player":
            #取得登入玩家資料
            res_message = self.getLoginedPlayer(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        else:
            #未定義的 message
            logging.error("Err: Undefined message.")
            res_message = Message("Undefined message.", {})
            self.sendResponseJsonMessage(400, res_message) # 狀態碼 400 -> 失敗
            
    # 將準備好的 message 物件解碼為 json 並回傳給 client
    def sendResponseJsonMessage(self, status_code, res_message):
        self.send_response(status_code) #狀態碼
        self.send_header("Content-type", "application/json; charset=utf-8") #header
        self.end_headers() #結束 headers 內容
        res_data = res_message.encoding_to_json() # message -> json(str)
        res_raw = res_data.encode('utf-8') # json(str) -> json(bytes)
        self.wfile.write(res_raw) #回覆 bytes 內容

    # test 1+1=2 (server 端透過 message 進行運算)
    def justfortest(self, message):
        """
            收到的 message 格式
            title = "just_for_test"
            contents = {"n1":1, "n2":1}
            回傳的 message 格式
            title = "just_for_test"
            contents = {"ans":2}
        """
        n1 = message.getContents()["n1"]
        n2 = message.getContents()["n2"]
        ans = n1 + n2
        ans_message = Message("just_for_test", {"ans":ans})
        return ans_message

    #建立新的玩家帳號
    def createPlayerAccount(self, message):
        """
            收到的 message 格式
            title = "create_player_account"
            contents = {"player_account":"xxxxxx", "player_hashed_password":"b64xxxxxxxx"}
            回傳的 message 格式
            title = "create_player_account"
            contents = {"status":0}
        """
        case = LockedCase()
        player_acc = message.getContents()["player_account"]
        encoded_hashed = message.getContents()["player_hashed_password"]
        hashed = base64.b64decode(encoded_hashed.encode("utf-8"))
        player_uuid = uuid.uuid1()
        status_code = case.createPlayerAccount(player_uuid, player_acc, hashed) #建立帳號完成
        ret_m = Message("create_player_account", {"status":status_code})
        return ret_m
    
    #帳號登入取得UUID
    def playerAccountLogin(self, message):
        """
            收到的 message 格式
            title = "player_account_login"
            contents = {"player_account":"xxxxxx", "player_trans_password":"b64xxxxxxxxx"}
            回傳的 message 格式
            title = "player_account_login"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
        """
        case = LockedCase()
        player_acc = message.getContents()["player_account"]
        tran_pw = message.getContents()["player_trans_password"]
        player_uuid = case.accountLoginValidate(player_acc, tran_pw) #登入取得 uuid
        if player_uuid == None:
            ret_m = Message("player_account_login", {})
        else:
            ret_m = Message("player_account_login", {"player_uuid":str(player_uuid)})
        return ret_m

    #取得登入玩家資料
    def getLoginedPlayer(self, message):
        """
            收到的 message 格式
            title = "get_logined_player"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
            回傳的 message 格式
            title = "get_logined_player"
            contents = {"player_name":"xxxxxx", "player_prestige":10}
        """
        case = LockedCase()
        player_uuid = message.getContents()["player_uuid"]
        ret_contents = case.getLoginedPlayerData(player_uuid)
        ret_m = Message("get_logined_player", ret_contents)
        return ret_m