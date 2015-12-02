"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import uuid
import os
import base64
from hashlib import sha256
from hmac import HMAC
"""
玩家 物件
"""
class Player:

    #建構子
    def __init__(self):
        self.account = None
        self.password = None
        self.hashedPassword = None
        self.player_uuid = None
        self.name = "" #名字
        self.prestige = 0 #聲望值 (若嫌惡值為0才會上升)
        self.gold = 0 #金幣
        self.disgust = 0 #嫌惡值 (行為不受其他玩家認同會上升)

    #設定玩家帳號
    def setPlayerAccount(self, account):
        # TODO 檢查 6-12 character a-z or A-Z or _ or number
        self.account = account
    
    #設定玩家密碼
    def setPlayerPassword(self, password):
        self.password = password
        # TODO 檢查 6-12 character a-z or A-Z or _ or number
    
    #設定加密過的玩家密碼
    def setHashedPlayerPassword(self, hashed):
        self.hashedPassword = hashed
        
    #設定 uuid (由server產生)
    def setPlayerUUID(self, player_uuid):
        if player_uuid.version == 1:
            self.player_uuid = player_uuid
            
    #取得 uuid
    def getPlayerUUID(self):
        if self.hasPlayerUUID():
            return self.player_uuid
        else:
            return None
    
    #檢查 有否 uuid
    def hasPlayerUUID(self):
        ret = False
        if self.player_uuid != None and self.player_uuid.version == 1:
            ret = True
        return ret
    
    # 密碼編碼 (在 client 端加密 再傳送 hashed)
    def encryptPassword(self, password, salt=None):
        if salt == None:
            salt = os.urandom(8)
        result = password.encode("utf-8")
        for i in range(10):
            result = HMAC(result, salt, sha256).digest()
        hashed = salt + result
        return hashed
        
    # 密碼驗証 (hashed 儲存在 server 端 trans_input_password 由 client 送出)
    def validatePassword(self, trans_input_password):
        input_password = base64.b64decode(trans_input_password.encode("utf-8")).decode("utf-8")
        return self.hashedPassword == self.encryptPassword(input_password, salt=self.hashedPassword[:8])
        
    #將輸入的密碼轉為密文再傳送
    def getTransInputPassword(self):
        return base64.b64encode(self.password.encode("utf-8")).decode("utf-8")
        