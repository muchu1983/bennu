# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import bennu.api.apis as apis
"""
測試 api 功能
"""
class ApiTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 幣別轉換 api
    def test_exchangeCurrency(self):
        logging.info("ApiTest.test_exchangeCurrency")
        print(apis.exchangeCurrency(fMoney=1000.0))
        print(apis.exchangeCurrency(fMoney=1000.0, strFrom="USD", strTo="USD"))
        print(apis.exchangeCurrency(fMoney=1000.0, strFrom="USD", strTo="TWD"))
        print(apis.exchangeCurrency(fMoney=1000.0, strFrom="TWD", strTo="USD"))
        print(apis.exchangeCurrency(fMoney=1000.0, strFrom="JPY", strTo="TWD"))

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


