"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""

import unittest
import logging
import time
import base64
import uuid
from united.player import Player
from united.world import World
from united.client import Client
from united.message import Message
from united.serverdb import SQLite3Db

"""
玩家建立帳號 功能測試
"""

class PlayerAccountTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_player = Player()
        self.default_world = World()
        self.default_cli = Client()
        self.default_world.startWorld()# 啟動 server
        time.sleep(2) #等待 2 秒讓 server 啟動完全
        
    #收尾
    def tearDown(self):
        self.default_player = None
        self.default_cli.closeConnection() #關閉 client 連線
        self.default_world.stopWorld() #關閉 server
        self.default_world = None
        self.default_cli = None

    #測試玩家 由 server 取得 uuid
    def test_player_acquire_uuid(self):
        logging.info("PlayerAccountTest.test_player_acquire_uuid")
        account = "MuChuHsu" # ui 讀入資料
        password = "united_is_OK"
        good_password = password
        bad_password = "united_ok_la"
        """
            收到的 message 格式
            title = "create_player_account"
            contents = {"player_account":"xxxxxx", "player_hashed_password":"b64xxxxxxxx"}
            回傳的 message 格式
            title = "create_player_account"
            contents = {"status":0}
        """
        #第一部份 建立帳號
        player_cli = Player()
        player_cli.setPlayerAccount(account)
        player_cli.setPlayerPassword(password)
        hashed = player_cli.encryptPassword(player_cli.password)
        player_cli.setHashedPlayerPassword(hashed)
        encoded_hashed = base64.b64encode(hashed).decode("utf-8")
        req_m = Message("create_player_account", {"player_account":player_cli.account,
                                                    "player_hashed_password":encoded_hashed})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("create_player_account", res_m.getTitle())
        self.assertEqual(0, res_m.getContents()["status"])

        """
            收到的 message 格式
            title = "player_account_login"
            contents = {"player_account":"xxxxxx", "player_trans_password":"b64xxxxxxxxx"}
            回傳的 message 格式
            title = "player_account_login"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
        """
        #第二部份 登入取得UUID
        player_cli.setPlayerPassword(good_password) #讀取輸入的密碼
        trans_pw = player_cli.getTransInputPassword()
        req_m = Message("player_account_login", {"player_account":player_cli.account,
                                                    "player_trans_password":trans_pw})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("player_account_login", res_m.getTitle())
        self.assertEqual(1, len(res_m.getContents().keys()))
        player_cli.setPlayerUUID(uuid.UUID(res_m.getContents()["player_uuid"]))
        self.assertTrue(player_cli.hasPlayerUUID())
        
    #取得登入玩家資料
    def test_get_logined_player(self):
        """
            收到的 message 格式
            title = "get_logined_player"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
            回傳的 message 格式
            title = "get_logined_player"
            contents = {"player_name":"xxxxxx", "player_prestige":10}
        """
        logging.info("PlayerAccountTest.test_get_logined_player")
        player_uuid = str(uuid.uuid1())
        player_acc = player_name = "test_player"
        db = SQLite3Db()
        db.insertOnePlayer([player_acc, "test_hashed".encode("utf-8"), player_uuid, player_name])
        req_m = Message("get_logined_player", {"player_uuid":player_uuid})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("get_logined_player", res_m.getTitle())
        self.assertEqual(player_name, res_m.getContents()["player_name"])
        self.assertEqual(0, res_m.getContents()["player_prestige"])

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


