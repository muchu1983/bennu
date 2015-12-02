"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.role import Role

"""
角色 模組測試
"""

class RoleTest(unittest.TestCase):

    #準備
    def setUp(self):
        self.default_role = Role("default_role", 0, 0)
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        self.default_role = None
        
    #測試生成物件
    def test_instance(self):
        logging.info("RoleTest.test_instance")
        self.assertIsInstance(self.default_role, Role)
        self.assertEqual("default_role", self.default_role.name)
        self.assertEqual(0, self.default_role.region_x)
        self.assertEqual(0, self.default_role.region_y)

#測試開始
if __name__ == "__main__":
    unittest.main()
