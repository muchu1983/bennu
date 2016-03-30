# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging

"""
測試 XXX
"""

class XXXXTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試XXX
    def test_xxx(self):
        logging.info("XXXXTest.test_xxx")

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


