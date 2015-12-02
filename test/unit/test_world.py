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

    #測試 啟動 World 2 秒後 關閉
    def test_start_world(self):
        logging.info("WorldTest.test_start_world")
        self.default_world.startWorld()
        time.sleep(2)
        self.default_world.stopWorld()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


