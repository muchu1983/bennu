"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import uuid
import base64
import time
from united.message import Message
from tkinter import Toplevel,Frame,Label,Entry,Button,Grid,Text

"""
超連結圖塊 資料輸入 視窗
"""
class HyperlinkToplevel:

    #建構子
    def __init__(self, master, gameboard, currentUrl, coords):
        self.canvas = master
        self.gameboard = gameboard
        topWidth = 400
        topHeight = 400
        self.hyperlinkTop = Toplevel(master)
        self.hyperlinkTop.grab_set()
        self.hyperlinkTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.hyperlinkTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        self.shape = "rectangel" #暫定 只提供矩型超連結
        self.masterUrl = currentUrl #擁有當前 hyperlink 的 url 圖片 (也可稱為 master url)
        self.coords = coords
        self.hyperlinkUrl = None #由玩家輸入 連結名稱
        self.description = "" #由玩家輸入 簡介
        #版面規劃
        hyperlinkTopTitleL = Label(self.hyperlinkTop, text="連結區塊資料")
        hyperlinkL = Label(self.hyperlinkTop, text="連結名稱")
        self.hyperlinkE = Entry(self.hyperlinkTop)
        descL = Label(self.hyperlinkTop, text="簡介")
        self.descT = Text(self.hyperlinkTop, padx=5, pady=5)
        okBtn = Button(self.hyperlinkTop, text="好", padx=5, pady=5, command=self.createHyperlink)
        hyperlinkTopTitleL.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="news")
        hyperlinkL.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="news")
        self.hyperlinkE.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="news")
        descL.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="news")
        self.descT.grid(row=3, column=0, rowspan=1, columnspan=2, sticky="news")
        okBtn.grid(row=4, column=0, rowspan=1, columnspan=2, sticky="news")
        Grid.rowconfigure(self.hyperlinkTop, 0 ,weight=1)
        Grid.rowconfigure(self.hyperlinkTop, 1 ,weight=1)
        Grid.rowconfigure(self.hyperlinkTop, 2 ,weight=1)
        Grid.rowconfigure(self.hyperlinkTop, 3 ,weight=10)
        Grid.rowconfigure(self.hyperlinkTop, 4 ,weight=1)
        Grid.columnconfigure(self.hyperlinkTop, 0 ,weight=0)
        Grid.columnconfigure(self.hyperlinkTop, 1 ,weight=1)
        
    def createHyperlink(self):
        self.hyperlinkUrl = self.hyperlinkE.get()
        self.description = self.descT.get(1.0, "end")
        self.canvas.addtag_withtag(self.hyperlinkUrl, "setting_hyperlink_area")
        self.canvas.dtag(self.hyperlinkUrl, "setting_hyperlink_area")
        data=(self.hyperlinkUrl,
              self.masterUrl,
              self.shape,
              self.coords,
              self.description)
        print(data)
        self.hyperlinkTop.destroy()
        