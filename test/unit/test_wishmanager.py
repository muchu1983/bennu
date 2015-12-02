"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.wishmanager import WishManager

"""
測試
"""

class WishManagerTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_wm = WishManager()
        
    #收尾
    def tearDown(self):
        self.default_wm = None

    #測試 建立實例
    def test_instance(self):
        logging.info("WishManagerTest.test_instance")
        self.assertIsInstance(self.default_wm, WishManager)
        

    #加入新願望
    def test_add_and_load_wish(self):
        logging.info("WishManagerTest.test_add_and_load_wish")
        wname = "New Wish"
        self.default_wm.addWish(wname+"1", "test1", "brief")
        self.default_wm.addWish(wname+"2", "test2", "brief")
        self.default_wm.addWish(wname+"3", "test3", "brief")
        self.assertTrue(len(self.default_wm.wish_dict.keys()) == 0)
        self.default_wm.loadWish()
        self.assertTrue(len(self.default_wm.wish_dict.keys()) > 0)
        self.assertEqual(self.default_wm.wish_dict["1"].name, wname+"1")
        self.assertEqual(self.default_wm.wish_dict["2"].name, wname+"2")
        self.assertEqual(self.default_wm.wish_dict["3"].name, wname+"3")


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


