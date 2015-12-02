"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import os
from united.emoji import Emoji

"""
測試 顏文字物件
"""

class EmojiTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 取得圖片
    def test_getImgPath(self):
        logging.info("EmojiTest.test_getImgPath")
        emoji = Emoji(":smile:")
        path = emoji.getImgPath()
        self.assertTrue(os.path.exists(path))

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


