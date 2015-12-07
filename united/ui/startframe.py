"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Frame,Button,Grid,Canvas,font
from united.ui.accounttoplevel import AccountToplevel
from PIL import Image,ImageTk
import os

"""
啟始頁
"""

class StartFrame:
    
    #建構子
    def __init__(self, master, gameboard):
        self.frame = Frame(master)
        self.board = gameboard
        self.bgImg = Image.open(os.getcwd() + "/united_res/bg.png")
        self.bgImgC = Canvas(self.frame)
        self.bgImgC.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="news")
        self.bgImgC.bind("<Configure>", self.settingBgImage)
        self.startBtn = Button(self.frame, font=font.Font(size=24), text="開始探索", state= "disable", command=self.switchToRegionPage)
        self.loginBtn = Button(self.frame, font=font.Font(size=24), text="登入帳號", command=self.board.checkAccountLogin)
        self.loginBtn.grid(row=1, column=1, padx=1, pady=1, sticky="s")
        self.startBtn.grid(row=2, column=1, padx=1, pady=1, sticky="n")
        Grid.rowconfigure(self.frame, 0, weight=1)
        Grid.rowconfigure(self.frame, 1, weight=1)
        Grid.rowconfigure(self.frame, 2, weight=1)
        Grid.rowconfigure(self.frame, 3, weight=1)
        Grid.columnconfigure(self.frame, 0, weight=1)
        Grid.columnconfigure(self.frame, 1, weight=1)
        Grid.columnconfigure(self.frame, 2, weight=1)
        
        
    #畫面資料更新
    def updatePageData(self):
        pass
        
    #顯示登入視窗
    def showAccountToplevel(self):
        accTop = AccountToplevel(self.frame, self.board)
        accTop.switchAccountPage("login_page")
        
    #啟動開始按鈕
    def activeStartBtn(self):
        self.startBtn.config(state="active")
        
    #切換到 區域頁
    def switchToRegionPage(self):
        self.board.setPageParam({})
        self.board.updatePageData("canvas_page")
        self.board.switchPage("canvas_page")
        
    #繪置背景圖
    def settingBgImage(self, event):
        cw = event.width / 2
        ch = event.height / 2
        self.bgTkimg = ImageTk.PhotoImage(image=self.bgImg.resize((event.width,event.height), Image.ANTIALIAS))
        self.bgImgC.create_image(cw, ch, image=self.bgTkimg)
        
