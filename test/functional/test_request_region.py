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
測試 client 取得 Region 的資料
"""

class RequestRegionTest(unittest.TestCase):

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

    #測試 取得區域資料
    def test_send_get_region_data(self):
        """
            收到的 message 格式
            title = "get_region_data"
            contents = {"region_name":"xxxxxx"}
            回傳的 message 格式
            title = "get_region_data"
            contents = {"0":"aaaaaa", "1":"bbbbbbb",...}
        """
        logging.info("RequestRegionTest.test_send_get_region_data")
        msg = Message("get_region_data", {"region_name":"sandbox"})
        res_m = self.default_cli.sendMessage(msg) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.assertEqual("get_region_data", res_m.getTitle())
        self.assertTrue(len(res_m.getContents().keys()) > 0)

    #測試 取得角色資料
    def test_send_get_role_data(self):
        """
            收到的 message 格式
            title = "get_role_data"
            contents = {"region_name":"xxxxxx", "role_name":"oooooo"}
            回傳的 message 格式
            title = "get_role_data"
            contents = {"name":"oooooooo", "region_x":100, "region_y":100, "dream_length":0}
        """
        logging.info("RequestRegionTest.test_send_get_role_data")
        msg = Message("get_role_data", {"region_name":"sandbox", "role_name":"muchu"})
        res_m = self.default_cli.sendMessage(msg) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.assertEqual("get_role_data", res_m.getTitle())
        self.assertTrue(len(res_m.getContents().keys()) >= 2) #至少要有 x,y
        self.assertEqual(0, res_m.getContents()["dream_length"])

    #測試 列出所有區域
    def test_list_all_region(self):
        """
            收到的 message 格式
            title = "list_all_region"
            contents = {"empty_contents":0}
            回傳的 message 格式
            title = "list_all_region"
            contents = {"0":"aaaaaa", "1":"bbbbbbb",...}
        """
        logging.info("RequestRegionTest.test_list_all_region")
        msg = Message("list_all_region", {"empty_contents":0})
        res_m = self.default_cli.sendMessage(msg) #送出 request
        self.assertTrue(res_m.isValid()) # 驗証回傳 message 格式是否正確
        self.assertEqual("list_all_region", res_m.getTitle())
        self.assertTrue(len(res_m.getContents().keys()) >= 1) #找到至少一個 region

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


