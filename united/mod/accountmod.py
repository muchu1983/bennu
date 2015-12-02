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

"""
使用者 註冊/登入 模組
"""
class AccountMod:

    #構構子
    def __init__(self):
        pass
        
    def dispatchMessage(self, message):
        message_title = message.getTitle()
        res_message = None
        if message_title == "create_player_account":
            #建立新的玩家帳號
            res_message = self.createPlayerAccount(message)
        elif message_title == "player_account_login":
            #帳號登入取得UUID
            res_message = self.playerAccountLogin(message)
        elif message_title == "get_logined_player":
            #取得登入玩家資料
            res_message = self.getLoginedPlayer(message)
        return res_message
        
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
