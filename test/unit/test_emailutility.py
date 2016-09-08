# -*- coding: utf-8 -*-
"""
Copyright (C) 2016, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import os
from bennu.emailutility import EmailUtility

"""
測試 EmailUtility
"""

class EmailUtilityTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.emailUtil = EmailUtility()
        
    #收尾
    def tearDown(self):
        pass

    #測試 寄信
    def test_sendEmail(self):
        logging.info("EmailUtilityTest.test_sendEmail")
        self.emailUtil.sendEmail(
            strSubject="unittest:bennu",
            strFrom="public.muchu1983",
            strTo="me",
            strMsg="內容：許公蓋",
            lstStrTarget=["muchu1983@gmail.com"],
            strSmtp="smtp.gmail.com:587",
            strAccount="public.muchu1983@gmail.com",
            strPassword="bee520520bee"
        )

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


