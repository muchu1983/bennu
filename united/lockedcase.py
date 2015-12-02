"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import uuid
import logging
from threading import Condition
from united.serverdb import SQLite3Db
from united.player import Player
"""
帶鎖箱
此類別附帶一個 Singleton 的鎖
寫在此類別下的方法，在 multithreading 情形下時
可以保證執行不會有重疊
"""

class LockedCase:

    #singleton
    __lock = Condition()

    #建構子
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        
    #取得 lock
    def getLock(self):
        return LockedCase.__lock

    #測試跑
    def testRun(self, num):
        self.getLock().acquire()
        pass
        self.getLock().release()

    #建立玩家帳號
    def createPlayerAccount(self, acc_uuid, account, hashed):
        self.getLock().acquire()
        db = SQLite3Db()
        #檢查是否有同名的帳號已存在
        exist = db.selectOnePlayer(account)
        ret = 1
        if exist == None:
            #建立帳號
            db.insertOnePlayer([account, hashed, str(acc_uuid), account])
            ret = 0
        else:
            logging.warning("Account name has already exist.")
            ret = 1
        self.getLock().release()
        return ret
        
    #帳號登入 成功返回 uuid 否則 None
    def accountLoginValidate(self, account, tran_pw):
        self.getLock().acquire()
        db = SQLite3Db()
        ret = None
        target = Player()
        player_data = db.selectOnePlayer(account)
        if player_data != None:
            target.setPlayerAccount(player_data[1])
            target.setHashedPlayerPassword(player_data[2])
            target.setPlayerUUID(uuid.UUID(player_data[3]))
            isValid = target.validatePassword(tran_pw)
            if isValid :ret = target.getPlayerUUID()
        self.getLock().release()
        return ret
        
    #取得登入玩家資料
    def getLoginedPlayerData(self, player_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        ret = {}
        player_data = db.selectUUIDPlayer(player_uuid)
        if player_data != None:
            ret["player_name"] = player_data[4]
            ret["player_prestige"] = player_data[5]
        self.getLock().release()
        return ret
        