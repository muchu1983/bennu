"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
import os
import base64
import json
from PIL import Image
from united.world import World
from united.client import Client
from united.message import Message
from united.serverdb import SQLite3Db

"""
測試 圖片相關 處理功能
"""

class ImageAccessTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        self.default_cli = Client()
        self.default_world.startWorld()# 啟動 server
        time.sleep(2) #等待 2 秒讓 server 啟動完全
        db = SQLite3Db()
        db.clearTable("image")
        db.clearTable("indextable")
        
    #收尾
    def tearDown(self):
        self.default_cli.closeConnection() #關閉 client 連線
        self.default_world.stopWorld() #關閉 server
        self.default_world = None
        self.default_cli = None
        
    #測試 發佈及載入 url 為 test 的圖片
    def test_post_and_load_image_data(self):
        logging.info("ImageAccessTest.test_post_and_load_image_data")
        default_url = "test"
        source_img = Image.open(os.getcwd() + "\\resource\\icon.jpg")
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "post_image_data"
            contents = {"url":"aaaaa",
                        "image_data":"b64xxxxxxxx",
                        "image_mode":"RGB",
                        "image_size":(w,h)}
            回傳的 message 格式
            title = "post_image_data"
            contents = {"status":0}
        """
        #第一部分 發佈圖片
        image_b64_data = base64.b64encode(source_img.tobytes()).decode("utf-8")
        req_m = Message("post_image_data", {"url":default_url,
                                            "image_data":image_b64_data,
                                            "image_mode":source_img.mode,
                                            "image_size":source_img.size})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("post_image_data", res_m.getTitle())
        self.assertEqual(0, res_m.getContents()["status"])
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "load_image_data"
            contents = {"url":"aaaaa"}
            回傳的 message 格式
            title = "load_image_data"
            contents = {"status":0,
                        "image_data":"b64xxxxxxxxxxxxx",
                        "image_mode":"RGB",
                        "image_size":(w,h)}
        """
        #第二部分 載入圖片
        req_m = Message("load_image_data", {"url":default_url})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("load_image_data", res_m.getTitle())
        self.assertEqual(0, res_m.getContents()["status"])
        ret_img_b64_data = res_m.getContents()["image_data"]
        ret_img_mode = res_m.getContents()["image_mode"]
        ret_img_size = res_m.getContents()["image_size"]
        ret_img = Image.frombytes(ret_img_mode, ret_img_size, base64.b64decode(ret_img_b64_data.encode("utf-8")))
        self.assertEqual(ret_img.size, source_img.size)
        self.assertEqual(ret_img.mode, source_img.mode)
        self.assertEqual(ret_img_b64_data, image_b64_data)
        
    #測試 建立 超連結 (root -> test) 並列出 root 下的所有超連結
    def test_create_and_list_hyperlink(self):
        logging.info("ImageAccessTest.test_create_and_list_hyperlink")
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "create_hyperlink"
            contents = {"hyperlink":"test",
                        "url":"root",
                        "json_coords":"[10,20,110,80]",
                        "shape":"rectangle",
                        "description":"XXXXXXXXXXXXX"}
            回傳的 message 格式
            title = "create_hyperlink"
            contents = {"status":0}
        """
        #第一部分 建立超連結
        req_m = Message("create_hyperlink", {"hyperlink":"test",
                                             "url":"root",
                                             "json_coords":json.dumps((10,20,110,80)),
                                             "shape":"rectangle",
                                             "description":"XXXXXXXXXXXXX"})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("create_hyperlink", res_m.getTitle())
        self.assertEqual(0, res_m.getContents()["status"])
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "list_hyperlink_on_url"
            contents = {"url":"aaaaa"}
            回傳的 message 格式
            title = "list_hyperlink_on_url"
            contents = {"status":0,
                        "hyperlink_list":[["hyperlink","json_coords","shape","description"],[...],...]}
        """
        #第二部分 列出 root url 下的所有 超連結
        req_m = Message("list_hyperlink_on_url", {"url":"root"})
        res_m = self.default_cli.sendMessage(req_m) #送出 request
        self.assertTrue(res_m.isValid())
        self.assertEqual("list_hyperlink_on_url", res_m.getTitle())
        self.assertEqual(0, res_m.getContents()["status"])
        self.assertEqual(1, len(res_m.getContents("hyperlink_list")))
        self.assertEqual("test", res_m.getContents("hyperlink_list")[0][0])

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


