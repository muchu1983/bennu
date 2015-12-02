"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.wish import Wish

"""
測試  願望
"""

class WishTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 建立實例
    def test_instance(self):
        logging.info("WishTest.test_instance")
        w = Wish(0, "name", "description str",  "brief target str")
        self.assertIsInstance(w, Wish)


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


