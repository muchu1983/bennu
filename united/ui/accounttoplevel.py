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
帳號 註冊與登入 視窗
"""
class AccountToplevel:

    #建構子
    def __init__(self, master, gameboard):
        self.gameboard = gameboard
        topWidth = 400
        topHeight = 200
        self.accountTop = Toplevel(master)
        self.accountTop.grab_set()
        self.accountTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.accountTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        self.loginFrame = Frame(self.accountTop)
        self.registerFrame = Frame(self.accountTop)
        self.loginFrame.grid(row=0, column=0, sticky="news")
        self.registerFrame.grid(row=0, column=0, sticky="news")
        self.accPage = {"login_page":self.loginFrame,"register_page":self.registerFrame}
        Grid.rowconfigure(self.accountTop, 0 ,weight=1)
        Grid.columnconfigure(self.accountTop, 0 ,weight=1)
        # login frame 版面規劃
        logL = Label(self.loginFrame, text="玩家登入")
        self.logStatusL = Label(self.loginFrame, text="status")
        logAccNameL = Label(self.loginFrame, text="輸入帳號")
        self.logAccNameE = Entry(self.loginFrame)
        logPassL = Label(self.loginFrame, text="輸入密碼")
        self.logPassE = Entry(self.loginFrame)
        loginBtn = Button(self.loginFrame, text="登入", command=self.accountLoginProcess)
        self.toRegFrameBtn = Button(self.loginFrame, text="註冊新帳號", command=self.toRegisterPage)
        logL.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="news")
        self.logStatusL.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="news")
        logAccNameL.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="news")
        self.logAccNameE.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        logPassL.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="news")
        self.logPassE.grid(row=3, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        loginBtn.grid(row=4, column=1, rowspan=1, columnspan=1, sticky="news")
        self.toRegFrameBtn.grid(row=5, column=1, rowspan=1, columnspan=1, sticky="news")
        Grid.grid_rowconfigure(self.loginFrame, 0 ,weight=1)
        Grid.grid_rowconfigure(self.loginFrame, 1 ,weight=0)
        Grid.grid_rowconfigure(self.loginFrame, 2 ,weight=1)
        Grid.grid_rowconfigure(self.loginFrame, 3 ,weight=1)
        Grid.grid_rowconfigure(self.loginFrame, 4 ,weight=1)
        Grid.grid_rowconfigure(self.loginFrame, 5 ,weight=0)
        Grid.grid_columnconfigure(self.loginFrame, 0 ,weight=0)
        Grid.grid_columnconfigure(self.loginFrame, 1 ,weight=1)
        # register frame 版面規劃
        regL = Label(self.registerFrame, text="註冊新帳號")
        self.regStatusL = Label(self.registerFrame, text="status")
        regAccNameL = Label(self.registerFrame, text="名稱")
        self.regAccNameE = Entry(self.registerFrame)
        regAccNameRuleL = Label(self.registerFrame, text="6-12字元:0-9|a-z|A-Z")
        regPass1L = Label(self.registerFrame, text="設定密碼")
        self.regPass1E = Entry(self.registerFrame)
        regPass2L = Label(self.registerFrame, text="密碼確認")
        self.regPass2E = Entry(self.registerFrame)
        regBtn = Button(self.registerFrame, text="送出註冊資料", command=self.sendRegisterDataAndSwitchPage)
        regL.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="news")
        self.regStatusL.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="news")
        regAccNameL.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="news")
        self.regAccNameE.grid(row=2, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        regAccNameRuleL.grid(row=3, column=1, rowspan=1, columnspan=1, sticky="news")
        regPass1L.grid(row=4, column=0, rowspan=1, columnspan=1, sticky="news")
        self.regPass1E.grid(row=4, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        regPass2L.grid(row=5, column=0, rowspan=1, columnspan=1, sticky="news")
        self.regPass2E.grid(row=5, column=1, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        regBtn.grid(row=6, column=1, rowspan=1, columnspan=2, sticky="news")
        Grid.grid_rowconfigure(self.registerFrame, 0 ,weight=1)
        Grid.grid_rowconfigure(self.registerFrame, 1 ,weight=0)
        Grid.grid_rowconfigure(self.registerFrame, 2 ,weight=1)
        Grid.grid_rowconfigure(self.registerFrame, 3 ,weight=0)
        Grid.grid_rowconfigure(self.registerFrame, 4 ,weight=1)
        Grid.grid_rowconfigure(self.registerFrame, 5 ,weight=1)
        Grid.grid_rowconfigure(self.registerFrame, 6 ,weight=0)
        Grid.grid_columnconfigure(self.registerFrame, 0 ,weight=0)
        Grid.grid_columnconfigure(self.registerFrame, 1 ,weight=1)
        
        
    #切換登入頁與註冊頁
    def switchAccountPage(self, acc_page_name):
        if acc_page_name in self.accPage:
            self.accPage[acc_page_name].tkraise()
        
    #切換到註冊頁面
    def toRegisterPage(self):
        self.switchAccountPage("register_page")
        
    #註冊成功返回登入頁面，否則留在註冊頁面
    def sendRegisterDataAndSwitchPage(self):
        player = self.gameboard.loginedPlayer
        input_acc = self.regAccNameE.get()
        input_pass1 = self.regPass1E.get()
        input_pass2 = self.regPass2E.get()
        if input_pass1 != input_pass2:
            self.regStatusL.config(text="兩次密碼輸入不相同。")
        else:
            player.setPlayerAccount(input_acc)
            player.setPlayerPassword(input_pass1)
            hashed = player.encryptPassword(input_pass1)
            player.setHashedPlayerPassword(hashed)
            encoded_hashed = base64.b64encode(hashed).decode("utf-8")
            req_m = Message("create_player_account", {"player_account":input_acc,
                                                        "player_hashed_password":encoded_hashed})
            res_m = self.gameboard.getClient().sendMessage(req_m) #送出 request
            if res_m.getContents()["status"] != 0: #檢查帳號建立是否成功
                self.regStatusL.config(text="無法建立此帳號。")
            else:
                self.logStatusL.config(text=input_acc + " 帳號建立成功。")
                self.logAccNameE.delete(0, "end")
                self.logAccNameE.insert(0, input_acc)
                self.toRegFrameBtn.config(state="disable")
                self.switchAccountPage("login_page")
        
    #執行登入作業
    def accountLoginProcess(self):
        player = self.gameboard.loginedPlayer
        input_acc = self.logAccNameE.get()
        input_pass = self.logPassE.get()
        player.setPlayerAccount(input_acc)
        player.setPlayerPassword(input_pass)
        trans_pw = player.getTransInputPassword()
        req_m = Message("player_account_login", {"player_account":input_acc,
                                                    "player_trans_password":trans_pw})
        res_m = self.gameboard.getClient().sendMessage(req_m) #送出 request
        if len(res_m.getContents().keys()) == 1:
            uuid_str = res_m.getContents()["player_uuid"]
            player.setPlayerUUID(uuid.UUID(uuid_str))
        self.gameboard.checkAccountLogin()
        self.accountTop.destroy()