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

    #建立新的 role
    def createNewRole(self, world, region_name, role_name, region_x, region_y):
        self.getLock().acquire()
        for re in world.region:
            if re.name == region_name:
                re.addRole(role_name, region_x, region_y)
                break
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
        
    #玩家將夢想附加到角色上
    def attachDreamToRole(self, world, region_name, role_name, wish_name, wish_desc, wish_brief, dreamer_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        dreamUUID = uuid.uuid1()
        for re in world.region:
            if re.name == region_name:
                for ro in re.role:
                    if ro.name == role_name:
                        ro.dreamIdList.append(str(dreamUUID))
                        break
                break
        realizerUUID = None
        state = 1
        award = 1
        db.insertOne("dream", [str(dreamUUID), dreamer_uuid, realizerUUID, state, wish_name, wish_desc, wish_brief, award, region_name, role_name])
        self.getLock().release()
        return 0
        
    # 玩家許下諾言將完成角色的夢想
    def realizerMakeAPromise(self, dream_uuid, realizer_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        db.updateSpecify("dream", {"realizerUUID":realizer_uuid, "state":2}, {"dreamUUID":dream_uuid})
        self.getLock().release()
        return 0
        
    # 玩家放棄任務
    def realizerAbortDreamPromise(self, dream_uuid, realizer_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        db.updateSpecify("dream", {"realizerUUID":None, "state":1}, {"dreamUUID":dream_uuid})
        self.getLock().release()
        return 0
        
    #角色夢想已完成
    def dreamerDreamComeTrue(self, dream_uuid, dreamer_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        if dreamData != None and dreamData[0][1] == dreamer_uuid:
            db.updateSpecify("dream", {"state":3}, {"dreamUUID":dream_uuid})
        self.getLock().release()
        return 0
    
    #實現者贏取獎勵
    def realizerAwardWinning(self, world, dream_uuid, realizer_uuid):
        self.getLock().acquire()
        db = SQLite3Db()
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        if dreamData != None and dreamData[0][2] == realizer_uuid:
            realizer_data = db.selectUUIDPlayer(realizer_uuid)
            new_award = dreamData[0][7] + realizer_data[5]
            db.updateSpecify("player", {"playerPrestige":new_award}, {"playerUUID":realizer_uuid})
            #刪除 dream
            region_name = dreamData[0][8]
            role_name = dreamData[0][9]
            for re in world.region:
                if re.name == region_name:
                    for ro in re.role:
                        if ro.name == role_name:
                            if dream_uuid in ro.dreamIdList:
                                ro.dreamIdList.remove(dream_uuid)
                            break
                    break
            db.deleteSpecify("dream", {"dreamUUID":dream_uuid})
        self.getLock().release()
        return 0
        
    #取得 夢想資料
    def getDreamData(self, dream_uuid):
        self.getLock().acquire()
        ret = {}
        db = SQLite3Db()
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        if len(dreamData) == 1:
            ret["dream_dreamer_uuid"] = dreamData[0][1]
            ret["dream_realizer_uuid"] = dreamData[0][2]
            ret["dream_state"] = dreamData[0][3]
            ret["dream_name"] = dreamData[0][4]
            ret["dream_description"] = dreamData[0][5]
            ret["dream_brief"] = dreamData[0][6]
            ret["dream_award"] = dreamData[0][7]
        self.getLock().release()
        return ret