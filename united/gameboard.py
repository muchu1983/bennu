"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Grid
from united.ui.startframe import StartFrame
from united.player import Player
import time

"""
GameBoard 控制 使用者主介面

gameboard 做為 MVC 中的控制角色
接收 View 角色的 Frame 的指令 向server送出 message
frame 不透過 gameboard 取得所需的資料
gameboard 將 提供 client  給 Frame 物件
由 Frame 物件 做View 角色 直接去 server 取得與顯示 資料
Client 物件 為 Model 角色
Client 提供方便的方法讓 gameboard 及 frame 用簡潔的 code 存取 world
"""
class GameBoard:

    #建構子
    def __init__(self, rootFrame):
        self.client = None #連線物件
        self.pageparam = None #頁面間參數 物件
        self.loginedPlayer = Player()
        #主框架
        self.root = rootFrame
        self.startPage = StartFrame(rootFrame, self)
        self.rootPage = {"start_page":self.startPage} # 分頁
        for pagekey in self.rootPage.keys():
            self.rootPage[pagekey].frame.grid(row=0, column=0, rowspan=3, columnspan=6, sticky="wens")
        self.switchPage("start_page") #切換至初始頁
        self.updatePageData("start_page")
        Grid.grid_rowconfigure(self.root, 0, weight=1)
        Grid.grid_columnconfigure(self.root, 0, weight=1)

    #切換分頁
    def switchPage(self, pagekey):
        if pagekey in self.rootPage:
            self.rootPage[pagekey].frame.tkraise()

    #更新分頁內容
    def updatePageData(self, pagekey):
        if pagekey in self.rootPage:
            self.rootPage[pagekey].updatePageData()
    
    #登入作業
    def checkAccountLogin(self):
        if True == self.loginedPlayer.hasPlayerUUID(): #已登入
            self.startPage.activeStartBtn()
        else: #未登入
            self.startPage.showAccountToplevel()
            
            
############### GET/SET ###########################
    #設定連線物件 Client
    def setClient(self, client):
        self.client = client

    #取得連線物件 Client
    def getClient(self):
        return self.client

    #設定 頁面間參數
    def setPageParam(self, param):
        self.pageparam = param
    #取得 頁面間參數
    def getPageParam(self):
        return self.pageparam
