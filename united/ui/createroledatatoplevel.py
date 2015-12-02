"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Toplevel,Label,Entry,Text,Button,Grid
from united.message import Message
from functools import partial
"""
新增角色 資料輸入視窗
"""

class CreateRoleDataToplevel:

    #構構子
    def __init__(self, master, region_name, anchorLoc, playframe):
        self.region_name = region_name
        self.anchorLoc = anchorLoc
        self.playframe = playframe
        topWidth = 300
        topHeight = 100
        self.roleDataTop = Toplevel(master)
        self.roleDataTop.grab_set()
        self.roleDataTop.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.roleDataTop.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        self.roleDataTop.title("輸入角色資訊")
        roleNameL = Label(self.roleDataTop, text="角色名稱")
        self.roleNameE = Entry(self.roleDataTop)
        descriptionL = Label(self.roleDataTop, text="角色描述")
        self.descriptionT = Text(self.roleDataTop)
        okBtn = Button(self.roleDataTop, text="Ok", command=self.createRole)
        roleNameL.grid(row=0, column=0, sticky="news")
        self.roleNameE.grid(row=0, column=1, padx=5, pady=5, sticky="news")
        #descriptionL.grid(row=1, column=0, columnspan=2, sticky="news")
        #self.descriptionT.grid(row=2, column=0, rowspan=2, columnspan=2, padx=5, pady=5, sticky="news")
        okBtn.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="news")
        Grid.grid_rowconfigure(self.roleDataTop, 0, weight=1)
        Grid.grid_rowconfigure(self.roleDataTop, 1, weight=1)
        Grid.grid_rowconfigure(self.roleDataTop, 2, weight=0)
        Grid.grid_rowconfigure(self.roleDataTop, 3, weight=0)
        Grid.grid_rowconfigure(self.roleDataTop, 4, weight=1)
        Grid.grid_columnconfigure(self.roleDataTop, 0, weight=0)
        Grid.grid_columnconfigure(self.roleDataTop, 1, weight=1)

    #建立 角色
    def createRole(self):
        role_name = self.roleNameE.get()
        description_text =  self.descriptionT.get(1.0, "end")
        self.roleDataTop.destroy() # 取得資訊後再關閉 Toplevel 視窗
        req_m = Message("create_new_role", {"region_name":self.region_name,
                                            "role_name":role_name,
                                            "region_x":self.anchorLoc[0],
                                            "region_y":self.anchorLoc[1]})
        res_m = self.playframe.board.getClient().sendMessage(req_m) #送出 request
        self.playframe.updatePageData()
