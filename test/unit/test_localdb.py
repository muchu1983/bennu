# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from bennu.localdb import MongoDb
"""
測試 本地端 Database
"""

class LocalDbTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.mongodb = MongoDb()
        
    #收尾
    def tearDown(self):
        pass

    #測試 取得 mongo db client
    def test_getMongoDbClient(self):
        logging.info("LocalDbTest.test_getMongoDbClient")
        self.assertIsNotNone(self.mongodb.getClient())

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


