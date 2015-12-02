"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Toplevel,Label,Button,ttk,Grid
from tkinter import Message as TkMessage
from united.message import Message
from functools import partial
"""
檢示 願望列表
"""
class DreamViewerToplevel:
    
    #建構子
    def __init__(self, master, gameboard, dream_id_list):
        self.gameboard = gameboard
        topWidth = 400
        topHeight = 300
        self.dreamViewerTop = Toplevel(master)
        self.dreamViewerTop.grab_set()
        self.dreamViewerTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.dreamViewerTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        self.nb = ttk.Notebook(self.dreamViewerTop)
        self.nb.grid(row=0, column=0, sticky="news")
        Grid.grid_rowconfigure(self.dreamViewerTop, 0, weight=1)
        Grid.grid_columnconfigure(self.dreamViewerTop, 0, weight=1)
        for dream_uuid in dream_id_list:
            self.createTabForDreamData(self.nb, dream_uuid)
            
    #由 dream uuid 取得 dream 資料
    def createTabForDreamData(self, notebook, dream_uuid):
        #取得 dream 資料
        req_m = Message("get_dream_data", {"dream_uuid":dream_uuid})
        res_m = self.gameboard.getClient().sendMessage(req_m)
        #建立 tab page
        notepage = ttk.Frame(notebook)
        stateCode = res_m.getContents()["dream_state"]
        dreamer_uuid = res_m.getContents()["dream_dreamer_uuid"]
        realizer_uuid_list = res_m.getContents()["dream_realizer_uuid_list"]
        dreamUUIDL = Label(notepage, text=dream_uuid)
        if realizer_uuid_list == None:
            realizerCount = 0
        else:
            realizerCount = len(realizer_uuid_list.split(","))
        realizerCountL = Label(notepage, text="接受人數:" + str(realizerCount))
        dreamStateL = Label(notepage, text="狀態碼:" + str(stateCode))
        dreamNameL = Label(notepage, text=res_m.getContents()["dream_name"])
        dreamDescM = TkMessage(notepage, text=res_m.getContents()["dream_description"])
        dreamBriefM = TkMessage(notepage, text=res_m.getContents()["dream_brief"])
        dreamAward = Label(notepage, text=str(res_m.getContents()["dream_award"]))
        acceptBtn = Button(notepage, text="無作用", state="disable", command=partial(self.makeAPromiseToDream, dream_uuid))
        abortBtn = Button(notepage, text="無作用", state="disable", command=partial(self.abortDreamPromise, dream_uuid))
        completedBtn = Button(notepage, text="無作用", state="disable", command=partial(self.dreamComeTrue, dream_uuid))
        awardBtn = Button(notepage, text="無作用", state="disable", command=partial(self.awardWinning, dream_uuid))
        dreamUUIDL.grid(row=0, column=0, columnspan=2, sticky="news")
        realizerCountL.grid(row=0, column=2, columnspan=1, sticky="news")
        dreamStateL.grid(row=0, column=3, columnspan=1, sticky="news")
        dreamNameL.grid(row=1, column=0, columnspan=4, sticky="news")
        dreamDescM.grid(row=2, column=0, columnspan=4, sticky="news")
        dreamBriefM.grid(row=3, column=0, columnspan=4, sticky="news")
        dreamAward.grid(row=4, column=3, columnspan=1, sticky="news")
        acceptBtn.grid(row=5, column=0, columnspan=1, sticky="news")
        abortBtn.grid(row=5, column=1, columnspan=1, sticky="news")
        completedBtn.grid(row=5, column=2, columnspan=1, sticky="news")
        awardBtn.grid(row=5, column=3, columnspan=1, sticky="news")
        Grid.grid_rowconfigure(notepage, 0, weight=0)
        Grid.grid_rowconfigure(notepage, 1, weight=0)
        Grid.grid_rowconfigure(notepage, 2, weight=1)
        Grid.grid_rowconfigure(notepage, 3, weight=1)
        Grid.grid_rowconfigure(notepage, 4, weight=0)
        Grid.grid_rowconfigure(notepage, 5, weight=1)
        Grid.grid_columnconfigure(notepage, 0, weight=1)
        Grid.grid_columnconfigure(notepage, 1, weight=1)
        Grid.grid_columnconfigure(notepage, 2, weight=1)
        Grid.grid_columnconfigure(notepage, 3, weight=1)
        
        #button 判定
        if stateCode == 1: #新的願望
            if dreamer_uuid != str(self.gameboard.loginPlayer.player_uuid):
                acceptBtn.config(state="active", text="接受托付")
            else:
                acceptBtn.config(state="disable", text="自己的願望")
        if stateCode == 2: #進行中的願望
            if dreamer_uuid == str(self.gameboard.loginPlayer.player_uuid):
                completedBtn.config(state="active", text="完成了")
            elif str(self.gameboard.loginPlayer.player_uuid) in realizer_uuid_list.split(","):
                abortBtn.config(state="active", text="放棄執行")
            else:
                acceptBtn.config(state="active", text="接受托付")
        if stateCode == 3: #已完成的願望
            if str(self.gameboard.loginPlayer.player_uuid) in realizer_uuid_list.split(","):
                awardBtn.config(state="active", text="領取獎勵")
        #加入 tab page
        notebook.add(notepage, text=res_m.getContents()["dream_name"])
        
    #玩家接受實現願望的任務
    def makeAPromiseToDream(self, dream_uuid):
        req_m = Message("make_a_promise", {"dream_uuid":dream_uuid,
                                            "realizer_uuid":str(self.gameboard.loginPlayer.player_uuid)})
        res_m = self.gameboard.getClient().sendMessage(req_m)
        self.dreamViewerTop.destroy()
        
    #玩家放棄任務
    def abortDreamPromise(self, dream_uuid):
        req_m = Message("abort_dream_promise", {"dream_uuid":dream_uuid,
                                            "realizer_uuid":str(self.gameboard.loginPlayer.player_uuid)})
        res_m = self.gameboard.getClient().sendMessage(req_m)
        self.dreamViewerTop.destroy()
        
    #玩家回達夢想已被完成了
    def dreamComeTrue(self, dream_uuid):
        req_m = Message("dream_come_true", {"dream_uuid":dream_uuid,
                                            "dreamer_uuid":str(self.gameboard.loginPlayer.player_uuid)})
        res_m = self.gameboard.getClient().sendMessage(req_m)
        self.dreamViewerTop.destroy()
    
    #玩家領取獎勵
    def awardWinning(self, dream_uuid):
        req_m = Message("award_winning", {"dream_uuid":dream_uuid,
                                          "realizer_uuid":str(self.gameboard.loginPlayer.player_uuid)})
        res_m = self.gameboard.getClient().sendMessage(req_m)
        self.dreamViewerTop.destroy()