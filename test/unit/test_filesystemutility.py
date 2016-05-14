# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import os
from bennu.filesystemutility import FileSystemUtility
"""
測試 FileSystemUtility
"""

class FileSystemUtilityTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.fsUtil = FileSystemUtility()
        
    #收尾
    def tearDown(self):
        pass

    #測試 取得 package 資源路徑
    def test_getPackageResourcePath(self):
        logging.info("FileSystemUtilityTest.test_getPackageResourcePath")
        strFileSystemPathOfResource = self.fsUtil.getPackageResourcePath(strPackageName="bennu_res", strResourceName="icon.ico")
        self.assertTrue(os.path.exists(strFileSystemPathOfResource))

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


