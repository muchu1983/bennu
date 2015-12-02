"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.message import Message

"""
測試 訊息 物件
"""

class MessageTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        pass

    #測試 檢查 格式
    def test_isvalid(self):
        logging.info("MessageTest.test_isvalid")
        m = Message("title", {"A":1, "B":2}) #正確範例
        self.assertTrue(m.isValid())
        m = Message("title", {"A":None, "B":2}) #正確範例 (None 值)
        self.assertTrue(m.isValid())
        m = Message(None, {"A":1, "B":2}) #title 不是 str 範例
        self.assertFalse(m.isValid())
        m = Message("title", None) #contents 不是 dict 範例
        self.assertFalse(m.isValid())
        m = Message("title", {"A":1, None:2}) # contents 含有非 str key 範例
        self.assertFalse(m.isValid())

    #測試 編碼
    def test_encoding_to_json(self):
        logging.info("MessageTest.test_encoding_to_json")
        m = Message("title", {"A":1, "B":2})
        encoded_m = m.encoding_to_json()
        self.assertTrue(type(encoded_m) is str)

    #測試 解碼
    def test_decoding_from_json(self):
        logging.info("MessageTest.test_decoding_from_json")
        m = Message("title", {"A":1, "B":2})
        encoded_str = m.encoding_to_json()
        new_m = Message(None, None) #格式 isValid 為 False
        self.assertFalse(new_m.isValid())
        new_m.decoding_from_json(encoded_str)
        self.assertTrue(new_m.isValid()) # 讀入 json 後變成 True
        
#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


