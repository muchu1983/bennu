"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""

import base64
import uuid
from united.message import Message
from united.lockedcase import LockedCase
from united.serverdb import SQLite3Db

"""
圖片資料 存取 模組
"""
class ImageDataMod:

    #構構子
    def __init__(self):
        pass
        
    def dispatchMessage(self, message):
        message_title = message.getTitle()
        res_message = None
        if message_title == "post_image_data":
            res_message = self.postImageData(message)
        elif message_title == "load_image_data":
            res_message = self.loadImageData(message)
        return res_message
        
    #發佈圖片資料
    def postImageData(self, message):
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "post_image_data"
            contents = {"link":"aaaaa",
                        "image_data":"b64xxxxxxxx",
                        "image_mode":"RGB",
                        "image_size":(w,h)}
            回傳的 message 格式
            title = "post_image_data"
            contents = {"status":0}
        """
        image_b64_data = message.getContents()["image_data"]
        image_bytes_data = base64.b64decode(image_b64_data.encode("utf-8"))
        db = SQLite3Db()
        db.insertOne("image", [None,
                               message.getContents()["link"],
                               image_bytes_data,
                               message.getContents()["image_mode"],
                               message.getContents()["image_size"][0],
                               message.getContents()["image_size"][1]])
        ret_m = Message("post_image_data", {"status":0})
        return ret_m
        
    #讀取圖片資料
    def loadImageData(self, message):
        """
            收到的 message 格式 (status 0->ok, 1->error)
            title = "load_image_data"
            contents = {"link":"aaaaa"}
            回傳的 message 格式
            title = "load_image_data"
            contents = {"status":0,
                        "image_data":"b64xxxxxxxxxxxxx",
                        "image_mode":"RGB",
                        "image_size":(w,h)}
        """
        ret_m = None
        db = SQLite3Db()
        img_data_list = db.selectSpecify("image", {"link":message.getContents()["link"]})
        if len(img_data_list) == 1: #正確 只有一筆相對應的圖片資料
            img_data = img_data_list[0]
            image_bytes_data = img_data[2]
            image_b64_data = base64.b64encode(image_bytes_data).decode("utf-8")
            ret_m = Message("load_image_data", {"status":0,
                                                "image_data":image_b64_data,
                                                "image_mode":img_data[3],
                                                "image_size":(img_data[4],img_data[5])})
        else:
            ret_m = Message("load_image_data", {"status":1})
        return ret_m
            