"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.jsonrequesthandler import JsonRequestHandler
from united.message import Message

"""
測試 Json-RPC 的 HTTP request 處理物件
"""

class JsonRequestHandlerTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        pass


    #測試 處理 just for test 1+1=2 訊息
    def test_justfortest(self):
        logging.info("JsonRequestHandlerTest.test_justfortest")
        req_m = Message("just_for_test", {"n1":1, "n2":1})
        res_m = JsonRequestHandler.justfortest(None, req_m)
        self.assertEqual(2, res_m.getContents()["ans"])

#測試開始
if __name__ == "__main__":
    unittest.main()


