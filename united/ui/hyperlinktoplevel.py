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
from tkinter import Toplevel,Frame,Label,Entry,Button,Grid,Text,StringVar

"""
超連結圖塊 資料輸入 視窗
"""
class HyperlinkToplevel:

    #建構子
    def __init__(self, master, canvasframe):
        topWidth = 400
        topHeight = 400
        self.canvasframe = canvasframe
        self.hyperlinkTop = Toplevel(master)
        self.hyperlinkTop.grab_set()
        self.hyperlinkTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.hyperlinkTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        #版面規劃
        self.varTitleStr = StringVar()
        self.varTitleStr.set("請輸入連結資料")
        hyperlinkTopTitleL = Label(self.hyperlinkTop, textvariable=self.varTitleStr)
        hyperlinkL = Label(self.hyperlinkTop, text="連結名稱")
        self.hyperlinkE = Entry(self.hyperlinkTop)
        descL = Label(self.hyperlinkTop, text="連結的描述")
        self.descT = Text(self.hyperlinkTop, padx=5, pady=5)
        okBtn = Button(self.hyperlinkTop, text="好", padx=5, pady=5, command=self.inputHyperlinkData)
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
        
    #輸入 hyperlink 資料
    def inputHyperlinkData(self):
        shape = "rectangel" #暫定 只提供矩型超連結
        hyperlinkUrl = self.hyperlinkE.get() #由玩家輸入的 連結名稱
        description = self.descT.get(1.0, "end") #由玩家輸入的 簡介
        if hyperlinkUrl == "" or description == None:
            self.varTitleStr.set("資料輸入不完整")
        else:
            self.hyperlinkTop.destroy()
            self.canvasframe.createHyperlink(shape, hyperlinkUrl, description)
        