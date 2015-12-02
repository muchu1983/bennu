"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
from test.unit.test_role import RoleTest
from test.unit.test_player import PlayerTest
from test.unit.test_world import WorldTest
from test.unit.test_region import RegionTest
from test.unit.test_httpserverthread import HttpServerThreadTest
from test.unit.test_jsonrequesthandler import JsonRequestHandlerTest
from test.unit.test_message import MessageTest
from test.unit.test_client import ClientTest
from test.unit.test_gameboard import GameBoardTest
from test.unit.test_lockedcase import LockedCaseTest
from test.unit.test_wish import WishTest
from test.unit.test_wishmanager import WishManagerTest
from test.unit.test_emoji import EmojiTest
"""
執行所有單元測試
"""
suite_of_all_unit = unittest.TestSuite()

#讀取 TestCase
suite_of_player = unittest.TestLoader().loadTestsFromTestCase(PlayerTest)
suite_of_role = unittest.TestLoader().loadTestsFromTestCase(RoleTest)
suite_of_world = unittest.TestLoader().loadTestsFromTestCase(WorldTest)
suite_of_region = unittest.TestLoader().loadTestsFromTestCase(RegionTest)
suite_of_httpserverthread = unittest.TestLoader().loadTestsFromTestCase(HttpServerThreadTest)
suite_of_jsonrequesthandler = unittest.TestLoader().loadTestsFromTestCase(JsonRequestHandlerTest)
suite_of_message = unittest.TestLoader().loadTestsFromTestCase(MessageTest)
suite_of_client = unittest.TestLoader().loadTestsFromTestCase(ClientTest)
suite_of_gameboard = unittest.TestLoader().loadTestsFromTestCase(GameBoardTest)
suite_of_lockedcase = unittest.TestLoader().loadTestsFromTestCase(LockedCaseTest)
suite_of_wish = unittest.TestLoader().loadTestsFromTestCase(WishTest)
suite_of_wishmanager = unittest.TestLoader().loadTestsFromTestCase(WishManagerTest)
suite_of_emoji = unittest.TestLoader().loadTestsFromTestCase(EmojiTest)

#加入 TestCase
suite_of_all_unit.addTest(suite_of_player)
suite_of_all_unit.addTest(suite_of_role)
suite_of_all_unit.addTest(suite_of_world)
suite_of_all_unit.addTest(suite_of_region)
suite_of_all_unit.addTest(suite_of_httpserverthread)
suite_of_all_unit.addTest(suite_of_jsonrequesthandler)
suite_of_all_unit.addTest(suite_of_message)
suite_of_all_unit.addTest(suite_of_client)
suite_of_all_unit.addTest(suite_of_gameboard)
suite_of_all_unit.addTest(suite_of_lockedcase)
suite_of_all_unit.addTest(suite_of_wish)
suite_of_all_unit.addTest(suite_of_wishmanager)
suite_of_all_unit.addTest(suite_of_emoji)

#執行測試
unittest.TextTestRunner().run(suite_of_all_unit)

