"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import uuid
import time
from united.player import Player
from united.world import World
from united.client import Client
from united.message import Message
from united.serverdb import SQLite3Db
from united.lockedcase import LockedCase

"""
測試 願望 的 起心動念、許下諾言、美夢成真、贏取獎勵 等動作
"""

class WishAccessTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.a_player = Player()
        self.a_player.setPlayerUUID(uuid.uuid1())
        self.b_player = Player()
        self.b_player.setPlayerUUID(uuid.uuid1())
        self.default_world = World()
        self.default_cli = Client()
        self.default_world.startHTTPServer()# 啟動 server
        time.sleep(2) #等待 2 秒讓 server 啟動完全
        
    #收尾
    def tearDown(self):
        self.a_player = None
        self.b_player = None
        self.default_cli.closeConnection() #關閉 client 連線
        self.default_world.stopHTTPServer() #關閉 server
        self.default_world = None
        self.default_cli = None

    #測試 起心動念 A玩家附加願望到角色裡
    def test_attach_dream_to_role(self):
        """
            收到的 message 格式
            title = "attach_dream"
            contents = {"region_name":"xxx",
                            "role_name":"ooo",
                            "wish_name":"dddd",
                            "wish_desc":"xxxxx",
                            "wish_brief":"bbbb",
                            "dreamer_uuid":"uuuu-uuuu-uu"}
            回傳的 message 格式
            title = "attach_dream"
            contents = {"status":0}
        """
        logging.info("WishAccessTest.test_attach_dream_to_role")
        dreamerUUID = uuid.uuid1()
        wish_name = "test_attach_dream_to_role"
        req_m = Message("attach_dream", {"region_name":"sandbox",
                                            "role_name":"muchu",
                                            "wish_name":wish_name,
                                            "wish_desc":"make united run and become popular game.",
                                            "wish_brief":"keep fight!",
                                            "dreamer_uuid":str(dreamerUUID)})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("attach_dream", res_m.getTitle())
        db = SQLite3Db()
        dreamData = db.selectSpecify("dream", {"region_name":"sandbox", "role_name":"muchu", "dreamName":wish_name})
        self.assertTrue(None != dreamData)
        self.assertEqual(1, len(dreamData))
        self.assertEqual(1, uuid.UUID(dreamData[0][0]).version) #server 建立的 dream UUID
        self.assertEqual(str(dreamerUUID), dreamData[0][1])
        self.assertEqual(1, dreamData[0][3]) #dream 目前的 狀態碼 == 1
        
    #測試 取得 願望資料讓 玩家檢視
    def test_get_dream_data(self):
        """
            收到的 message 格式
            title = "get_dream_data"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd"}
            回傳的 message 格式
            title = "get_dream_data"
            contents = {"dream_name":"xxxxxxxx",
                        "dream_description":"xxxxxxx",
                        "dream_brief":"xxxxxxxxxxxx"
                        "dream_award":10,
                        "dream_state":1,
                        "dream_dreamer_uuid":"ddddd-ddd-dd-dddd",
                        "dream_realizer_uuid":"rrrrr-rrr-rr-rr"}
        """
        #準備測試資料
        dream_uuid = str(uuid.uuid1())
        dreamer_uuid = str(uuid.uuid1())
        realizer_uuid = None
        db = SQLite3Db()
        db.insertOne("dream", [dream_uuid, dreamer_uuid, realizer_uuid, 1, "test_get_dream_data", "get_test", "get_test", 10, "sandbox", "muchu"])
        req_m = Message("get_dream_data", {"dream_uuid":dream_uuid})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("get_dream_data", res_m.getTitle())
        self.assertEqual("test_get_dream_data", res_m.getContents()["dream_name"])
        self.assertEqual("get_test", res_m.getContents()["dream_description"])
        self.assertEqual("get_test", res_m.getContents()["dream_brief"])
        self.assertEqual(1, res_m.getContents()["dream_state"])
        self.assertEqual(dreamer_uuid, res_m.getContents()["dream_dreamer_uuid"])
        self.assertEqual(realizer_uuid, res_m.getContents()["dream_realizer_uuid"])
        
    #測試 許下諾言 B玩家接受達成願望的任務
    def test_make_a_promise(self):
        """
            收到的 message 格式
            title = "make_a_promise"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd",
                        "realizer_uuid":"rrrr-rrrr-rrrr"}
            回傳的 message 格式
            title = "make_a_promise"
            contents = {"status":0}
        """
        logging.info("WishAccessTest.test_make_a_promise")
        #準備測試資料
        dream_uuid = str(uuid.uuid1())
        dreamer_uuid = str(uuid.uuid1())
        realizer_uuid = str(uuid.uuid1())
        db = SQLite3Db()
        db.insertOne("dream", [dream_uuid, dreamer_uuid, None, 1, "test_make_a_promise", "", "", 10, "sandbox", "muchu"])
        #進行測試
        req_m = Message("make_a_promise", {"dream_uuid":dream_uuid, "realizer_uuid":realizer_uuid})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("make_a_promise", res_m.getTitle())
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        self.assertEqual(1, len(dreamData))
        self.assertEqual(2, dreamData[0][3]) #檢查狀態碼 1->2
        self.assertEqual(realizer_uuid, dreamData[0][2]) #檢查 實現者 UUID
        
    #測試 放棄任務 玩家放棄繼續執行任務
    def test_abort_dream_promise(self):
        """
            收到的 message 格式
            title = "abort_dream_promise"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd",
                        "realizer_uuid":"rrrr-rrrr-rrrr"}
            回傳的 message 格式
            title = "abort_dream_promise"
            contents = {"status":0}
        """
        logging.info("WishAccessTest.test_abort_dream_promise")
        #準備測試資料
        dream_uuid = str(uuid.uuid1())
        dreamer_uuid = str(uuid.uuid1())
        realizer_uuid = str(uuid.uuid1())
        db = SQLite3Db()
        db.insertOne("dream", [dream_uuid, dreamer_uuid, realizer_uuid, 2, "test_abort_dream_promise", "", "", 10, "sandbox", "muchu"])
        #進行測試
        req_m = Message("abort_dream_promise", {"dream_uuid":dream_uuid, "realizer_uuid":realizer_uuid})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("abort_dream_promise", res_m.getTitle())
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        self.assertEqual(1, len(dreamData))
        self.assertEqual(1, dreamData[0][3]) #檢查狀態碼 2->1
        self.assertEqual(None, dreamData[0][2]) #檢查 實現者 UUID 已刪除
        
    #測試 美夢成真 A玩家答覆願望已完成
    def test_dream_come_true(self):
        """
            收到的 message 格式
            title = "dream_come_true"
            contents = {"dream_uuid":"ddddd-dddd-dddddd",
                        "dreamer_uuid":"uuuu-uuuuu-uuu"}
            回傳的 message 格式
            title = "dream_come_true"
            contents = {"status":0}
        """
        logging.info("WishAccessTest.test_dream_come_true")
        #準備測試資料
        dream_uuid = str(uuid.uuid1())
        dreamer_uuid = str(uuid.uuid1())
        realizer_uuid = str(uuid.uuid1())
        db = SQLite3Db()
        db.insertOne("dream", [dream_uuid, dreamer_uuid, realizer_uuid, 2, "test_dream_come_true", "", "", 10, "sandbox", "muchu"])
        #進行測試
        req_m = Message("dream_come_true", {"dream_uuid":dream_uuid, "dreamer_uuid":dreamer_uuid})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("dream_come_true", res_m.getTitle())
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        self.assertEqual(1, len(dreamData))
        self.assertEqual(3, dreamData[0][3]) #檢查狀態碼 2->3
        
        
    #測試 贏取獎勵 B玩家取得獎勵
    def test_award_winning(self):
        """
            收到的 message 格式
            title = "award_winning"
            contents = {"dream_uuid":"ddddd-dddd-dddddd",
                        "realizer_uuid":"rrrrr-rrrr-rrrrr"}
            回傳的 message 格式
            title = "award_winning"
            contents = {"status":0}
        """
        logging.info("WishAccessTest.test_award_winning")
        #準備測試資料
        dream_uuid = str(uuid.uuid1())
        dreamer_uuid = str(uuid.uuid1())
        realizer_uuid = str(uuid.uuid1())
        realizer_acc = "test_acc"
        award = 3
        db = SQLite3Db()
        test_hashed = "test_hashed".encode("utf-8")
        db.insertOnePlayer([realizer_acc, test_hashed, realizer_uuid, "test_realizer"])
        db.insertOne("dream", [dream_uuid, dreamer_uuid, realizer_uuid, 3, "test_award_winning", "", "", award, "sandbox", "muchu"])
        #進行測試
        req_m = Message("award_winning", {"dream_uuid":dream_uuid, "realizer_uuid":realizer_uuid})
        res_m = self.default_cli.sendMessage(req_m)
        self.assertTrue(res_m.isValid())
        self.assertEqual("award_winning", res_m.getTitle())
        dreamData = db.selectSpecify("dream", {"dreamUUID":dream_uuid})
        self.assertEqual([], dreamData)
        #測試 realizer 得到 獎勵
        ret_player_data = db.selectOnePlayer(realizer_acc)
        self.assertTrue(ret_player_data != None)
        self.assertEqual(award, ret_player_data[5])
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


