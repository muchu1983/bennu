"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
from united.client import Client
from united.world import World
from united.message import Message

"""
測試 client 端
"""

class ClientTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        self.default_cli = Client()
        
    #收尾
    def tearDown(self):
        self.default_world = None
        self.default_cli = None

    #測試 instance
    def test_instance(self):
        logging.info("ClientTest.test_instance")
        self.assertIsInstance(self.default_cli, Client)

    #測試 送出訊息
    def test_sendMessage(self):
        """
            收到的 message 格式
            title = "just_for_test"
            contents = {"n1":1, "n2":1}
            回傳的 message 格式
            title = "just_for_test"
            contents = {"ans":2}
        """
        logging.info("ClientTest.test_sendMessage")
        self.default_world.startHTTPServer()# 啟動 server
        time.sleep(5) #等待 5 秒讓 server 啟動完全
        justfortest_m = Message("just_for_test", {"n1":1, "n2":1})
        res_m = self.default_cli.sendMessage(justfortest_m) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.default_cli.closeConnection() #關閉連線
        self.default_world.stopHTTPServer() #關閉 server

#測試開始
if __name__ == "__main__":
    unittest.main()


