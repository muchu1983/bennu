"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.region import Region

"""
測試 地區
"""

class RegionTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_region = Region("default")
        
    #收尾
    def tearDown(self):
        self.default_region = None

    #測試生成物件
    def test_instance(self):
        logging.info("RegionTest.test_instance")
        self.assertEqual(self.default_region.name, "default")

    #測試在區域中加入角色
    def test_addRole(self):
        logging.info("RegionTest.test_addRole")
        self.default_region.addRole("my Queen", 0, 0)
        self.assertTrue(len(self.default_region.role) > 0)
        self.assertEqual("my Queen", self.default_region.role[0].name)

    #測試 找出最靠近的 role
    def test_findCloestRole(self):
        logging.info("RegionTest.test_findCloestRole")
        self.default_region.addRole("1", 10, 10)
        self.default_region.addRole("2", 20, 10)
        self.default_region.addRole("9", 90, 90)
        self.assertEqual("1", self.default_region.findCloestRole(5, 10).name)
        self.assertEqual("1", self.default_region.findCloestRole(12, 10).name)
        self.assertEqual("2", self.default_region.findCloestRole(16, 10).name)
        self.assertEqual("2", self.default_region.findCloestRole(22, 10).name)
        self.assertEqual("1", self.default_region.findCloestRole(15, 10).name) # 同距離時取第一個
        self.assertEqual(None, self.default_region.findCloestRole(15, 30)) # 最遠取得距離 20 pixel

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


