# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from bennu.externaldb import CameoMongoDb
"""
測試 外部 Mongo Database
"""

class MongoDbTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.cameoDb = CameoMongoDb()
        
    #收尾
    def tearDown(self):
        pass

    #測試 取得 client
    def test_getClient(self):
        logging.info("MongoDbTest.test_getClient")
        self.assertIsNotNone(self.cameoDb.getClient())

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


