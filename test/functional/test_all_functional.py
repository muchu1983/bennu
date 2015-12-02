"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
from test.functional.test_player_account import PlayerAccountTest
from test.functional.test_gameboard_show import GameboardShowTest
from test.functional.test_image_access import ImageAccessTest

"""
執行所有功能測試
"""
suite_of_all_functional = unittest.TestSuite()

#讀取 TestCase
suite_of_player_account = unittest.TestLoader().loadTestsFromTestCase(PlayerAccountTest)
suite_of_gameboard_show = unittest.TestLoader().loadTestsFromTestCase(GameboardShowTest)
suite_of_image_access = unittest.TestLoader().loadTestsFromTestCase(ImageAccessTest)

#加入 TestCase
suite_of_all_functional.addTest(suite_of_player_account)
suite_of_all_functional.addTest(suite_of_gameboard_show)
suite_of_all_functional.addTest(suite_of_image_access)

#執行測試
unittest.TextTestRunner().run(suite_of_all_functional)

