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
from tkinter import Toplevel,Frame,Label,Entry,Button,Grid

"""
超連結圖塊 資料輸入 視窗
"""
class HyperlinkToplevel:

    #建構子
    def __init__(self, master, gameboard):
        self.gameboard = gameboard
        topWidth = 400
        topHeight = 200
        self.hyperlinkTop = Toplevel(master)
        self.hyperlinkTop.title("連結區塊資料")
        self.hyperlinkTop.grab_set()
        self.hyperlinkTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.hyperlinkTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        
        
        Grid.rowconfigure(self.hyperlinkTop, 0 ,weight=1)
        Grid.columnconfigure(self.hyperlinkTop, 0 ,weight=1)
        
        