"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
from test.functional.test_player_account import PlayerAccountTest
from test.functional.test_request_region import RequestRegionTest
from test.functional.test_gameboard_show import GameboardShowTest
from test.functional.test_request_role import RequestRoleTest
from test.functional.test_wish_access import WishAccessTest

"""
執行所有功能測試
"""
suite_of_all_functional = unittest.TestSuite()

#讀取 TestCase
suite_of_player_account = unittest.TestLoader().loadTestsFromTestCase(PlayerAccountTest)
suite_of_req_region = unittest.TestLoader().loadTestsFromTestCase(RequestRegionTest)
suite_of_gameboard_show = unittest.TestLoader().loadTestsFromTestCase(GameboardShowTest)
suite_of_request_role = unittest.TestLoader().loadTestsFromTestCase(RequestRoleTest)
suite_of_wish_access = unittest.TestLoader().loadTestsFromTestCase(WishAccessTest)

#加入 TestCase
suite_of_all_functional.addTest(suite_of_player_account)
suite_of_all_functional.addTest(suite_of_req_region)
suite_of_all_functional.addTest(suite_of_gameboard_show)
suite_of_all_functional.addTest(suite_of_request_role)
suite_of_all_functional.addTest(suite_of_wish_access)

#執行測試
unittest.TextTestRunner().run(suite_of_all_functional)

