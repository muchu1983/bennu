"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.gameboard import GameBoard
from united.client import Client
from tkinter import Frame,Button,Tk

"""
測試 使用者界面 GameBoard
"""

class GameBoardTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        pass

    #widget 測試 切換 frame 頁面 (直接手動關閉)
    def test_change_frame_page(self):
        logging.info("GameBoardTest.test_change_frame_page")
        frame = Tk()
        frame.title("test_change_frame_page")
        frame.geometry("100x150")
        page1 = Frame(frame, bg="red", width=100, height=100)
        page2 = Frame(frame, bg="yellow", width=100, height=100)
        page3 = Frame(frame, bg="green", width=100, height=100)
        page1.grid(row=0, column=0)
        page2.grid(row=0, column=0)
        page3.grid(row=0, column=0)
        pages = {"1":page1, "2":page2, "3":page3}
        self.curpage = 1
        def nextPage():
            pages[str(self.curpage)].tkraise()
            self.curpage+=1
            if self.curpage > 3:
                self.curpage -= 3
        btn = Button(frame, bg="white", text="first", command=nextPage)
        btn.grid(row=1, column=0)
        frame.mainloop()

    #測試 get & set Client物件
    def test_get_and_set_client(self):
        logging.info("GameBoardTest.test_get_and_set_client")
        frame = Tk()
        frame.title("test_get_and_set_client")
        board = GameBoard(frame)
        frame.destroy()
        client = Client()
        self.assertTrue(board.getClient() == None)
        board.setClient(client)
        self.assertIs(board.getClient(), client)

    #測試 get & set pageparam 物件 該物件做為 各頁面間的參數傳遞
    def test_get_and_set_pageparam(self):
        logging.info("GameBoardTest.test_get_and_set_pageparam")
        frame = Tk()
        frame.title("test_get_and_set_pageparam")
        board = GameBoard(frame)
        frame.destroy()
        self.assertTrue(board.getPageParam() == None)
        strobj = "string obj"
        intobj = 0
        dictobj = {"str":1}
        arrobj = [1, 2, 3]
        board.setPageParam(strobj)
        self.assertIs(strobj, board.getPageParam())
        board.setPageParam(intobj)
        self.assertIs(intobj, board.getPageParam())
        board.setPageParam(dictobj)
        self.assertIs(dictobj, board.getPageParam())
        board.setPageParam(arrobj)
        self.assertIs(arrobj, board.getPageParam())
        
#測試開始
if __name__ == "__main__":
    unittest.main()


