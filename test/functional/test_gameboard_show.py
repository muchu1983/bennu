"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
from united.world import World
from united.client import Client
from united.gameboard import GameBoard
from tkinter import Tk,Frame,Grid

"""
測試 遊戲板 從 server 取得資料顯示
"""

class GameboardShowTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.default_world = World()
        self.P1_cli = Client()
        self.P2_cli = Client()
        self.default_world.startWorld()# 啟動 server
        time.sleep(2) #等待 2 秒讓 server 啟動完全
        
    #收尾
    def tearDown(self):
        self.P1_cli.closeConnection() #關閉 client 1 連線
        self.P2_cli.closeConnection() #關閉 client 2 連線
        self.default_world.stopWorld() #關閉 server
        self.default_world.saveWorldToDb() #儲存 world 資料
        self.default_world = None
        self.P1_cli = None
        self.P2_cli = None
        
    #測試 顯示 一組 gameboard client
    def test_show_1_gameboard(self):
        logging.info("GameboardShowTest.test_show_1_gameboard")
        root = Tk()
        p1 = Frame(root)
        board1 = GameBoard(p1)
        board1.setClient(self.P1_cli)
        p1.grid(row=0, column=0, sticky="news")
        root.wm_state("zoom") #最大化
        root.resizable(0,0) #關閉調整大小
        Grid.grid_rowconfigure(root, 0, weight=1)
        Grid.grid_columnconfigure(root, 0, weight=1)
        root.mainloop()

    #測試 顯示 兩組 gameboard client
    def test_show_2_gameboard(self):
        logging.info("GameboardShowTest.test_show_2_gameboard")
        root = Tk()
        #P1
        p1 = Frame(root)
        board1 = GameBoard(p1)
        board1.setClient(self.P1_cli)
        p1.grid(row=0, column=0, sticky="news")
        #P2
        p2 = Frame(root)
        board2 = GameBoard(p2)
        board2.setClient(self.P2_cli)
        p2.grid(row=0, column=1, sticky="news")
        root.wm_state("zoom") #最大化
        root.resizable(0,0) #關閉調整大小
        Grid.grid_rowconfigure(root, 0, weight=1)
        Grid.grid_columnconfigure(root, 0, weight=1)
        Grid.grid_columnconfigure(root, 1, weight=1)
        root.mainloop()

#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


