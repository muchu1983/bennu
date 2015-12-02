"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
from united.world import World
from united.client import Client
from united.message import Message

"""
測試 client 建立與修改 Role 的資料
"""

class RequestRoleTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        self.default_cli = Client()
        self.default_world.startHTTPServer()# 啟動 server
        time.sleep(2) #等待 2 秒讓 server 啟動完全
        
    #收尾
    def tearDown(self):
        self.default_cli.closeConnection() #關閉 client 連線
        self.default_world.stopHTTPServer() #關閉 server
        self.default_world = None
        self.default_cli = None

    #測試 建立新的 role
    def test_create_new_role(self):
        """
            收到的 message 格式
            title = "create_new_role"
            contents = {"region_name":"xxx", "role_name":"ooo", "region_x":300, "region_y":200}
            回傳的 message 格式
            title = "create_new_role"
            contents = {"status":0}
        """
        logging.info("RequestRoleTest.test_create_new_role")
        req_m = Message("create_new_role", {"region_name":"sandbox", "role_name":"blue ant amound", "region_x":300, "region_y":200})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.assertEqual("create_new_role", res_m.getTitle())
        
    #測試 找出最靠近的 角色
    def test_find_cloest_role(self):
        """
            收到的 message 格式
            title = "find_cloest_role"
            contents = {"region_name":"xxxxx", "region_x":123, "region_y":321}
            回傳的 message 格式
            title = "find_cloest_role"
            contents = {"role_name":"role_name", "dream_list":["aaa-aaa","bbb-bbb-b"]}
        """
        logging.info("RequestRoleTest.test_find_cloest_role")
        req_m = Message("find_cloest_role", {"region_name":"sandbox", "region_x":105, "region_y":105}) # role "muchu" 位置是(100,100)
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.assertEqual("find_cloest_role", res_m.getTitle())
        self.assertEqual("muchu", res_m.getContents()["role_name"])
        self.assertEqual([], res_m.getContents()["dream_list"])
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


