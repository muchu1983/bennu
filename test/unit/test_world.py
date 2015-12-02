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

"""
測試 世界物件
"""

class WorldTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        
    #收尾
    def tearDown(self):
        self.default_world = None
        
    #測試 預設區域
    def test_default_region(self):
        logging.info("WorldTest.test_default_region")
        self.assertTrue(len(self.default_world.region) > 0)

    #測試 啟動http server 5 秒後 關閉
    def test_start_http_server(self):
        logging.info("WorldTest.test_start_http_server")
        self.default_world.startHTTPServer()
        time.sleep(5)
        self.default_world.stopHTTPServer()

#測試開始
if __name__ == "__main__":
    unittest.main()


