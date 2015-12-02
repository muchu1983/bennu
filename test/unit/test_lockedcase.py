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
from threading import Thread
from united.lockedcase import LockedCase
from united.world import World
from united.player import Player

"""
測試 帶鎖箱 Multithreading 時確保箱內的方法執行不重疊
"""

class LockedCaseTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        
    #收尾
    def tearDown(self):
        self.defualt_world = None

    #測試 lock 是 Singleton 的
    def test_singleton_condition_lock(self):
        logging.info("LockedCaseTest.test_singleton_condition_lock")
        case1 = LockedCase()
        case2 = LockedCase()
        case3 = LockedCase()
        self.assertIs(case1.getLock(), case2.getLock()) # 1 is 2
        self.assertIs(case2.getLock(), case3.getLock()) # 2 is 3
        self.assertIs(case3.getLock(), case1.getLock()) # 3 is 1
        self.assertIs(case1.getLock(), case1.getLock()) # 1 is 1
        self.assertIs(case2.getLock(), case2.getLock()) # 2 is 2
        self.assertIs(case3.getLock(), case3.getLock()) # 3 is 3

    # 測試 多執行緒 的情形下 lock 的作用
    def test_multithreading_effect(self):
        logging.info("LockedCaseTest.test_multithreading_effect")
        case = LockedCase()
        class CaseRunner(Thread):
            def __init__(self, num):
                Thread.__init__(self)
                self.num = num
            def run(self):
                case = LockedCase()
                case.testRun(self.num)
        for i in range(20):
            cr = CaseRunner(str(i))
            cr.start()
        
    #測試 創建新帳號
    def test_create_player_account(self):
        logging.info("LockedCaseTest.test_create_player_account")
        case = LockedCase()
        account = "myAccount"
        password = "123456789012"
        player = Player()
        player.setPlayerPassword(password)
        hashed = player.encryptPassword(player.password)
        acc_uuid = uuid.uuid1()
        case.createPlayerAccount(acc_uuid, account, hashed) #建立帳號完成
        #進行登入驗証
        tran_pw = player.getTransInputPassword()
        ret_uuid = case.accountLoginValidate(account, tran_pw) #登入取得 uuid
        self.assertTrue(acc_uuid == ret_uuid)
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


