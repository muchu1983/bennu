# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
#from test.unit.test_XXX import XXXTest

"""
執行所有單元測試
"""
suite_of_all_unit = unittest.TestSuite()

#讀取 TestCase
#suite_of_XXX = unittest.TestLoader().loadTestsFromTestCase(XXXTest)

#加入 TestCase
#suite_of_all_unit.addTest(suite_of_XXX)

#執行測試
unittest.TextTestRunner().run(suite_of_all_unit)

