"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import uuid
from united.player import Player

"""
玩家 模組測試
"""

class PlayerTest(unittest.TestCase):

    #準備
    def setUp(self):
        self.default_player = Player()
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        self.default_player = None

    #測試生成玩家物件
    def test_instance(self):
        logging.info("PlayerTest.test_instance")
        self.assertIsInstance(self.default_player, Player)

    #測試設定玩家名稱
    def test_set_player_account(self):
        logging.info("PlayerTest.test_set_player_account")
        self.default_player.setPlayerAccount("Somebody")
        self.default_player.setPlayerPassword("123456789012")
        self.assertEqual(self.default_player.account, "Somebody")
        self.assertEqual(self.default_player.password, "123456789012")

    #檢查是否有uuid
    def test_hasUUID(self):
        logging.info("PlayerTest.test_hasUUID")
        self.assertFalse(self.default_player.hasPlayerUUID())
        self.default_player.setPlayerUUID(uuid.uuid1())
        self.assertTrue(self.default_player.hasPlayerUUID())
    
    #密碼加密及驗証
    def test_password_encrypt_and_validate(self):
        logging.info("PlayerTest.test_password_encrypt_and_validate")
        raw_pw = "123456789012"
        bad_pw = "123"
        self.default_player.setPlayerPassword(raw_pw)
        hashed = self.default_player.encryptPassword(self.default_player.password) #加密 hashed -> server (client)
        self.default_player.setHashedPlayerPassword(hashed) # 取得 serverdb 的 hashed 
        good_tran_pw = self.default_player.getTransInputPassword() #base64 code -> server (client)
        isValid = self.default_player.validatePassword(good_tran_pw) # server 比對 hashed 與 trans_pw (server)
        self.assertTrue(isValid)
        self.default_player.setPlayerPassword(bad_pw)
        bad_tran_pw = self.default_player.getTransInputPassword() #base64 code -> server (client)
        isValid = self.default_player.validatePassword(bad_tran_pw) # server 比對 hashed 與 trans_pw (server)
        self.assertFalse(isValid)

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


