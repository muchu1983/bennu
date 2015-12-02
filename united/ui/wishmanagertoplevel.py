"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Toplevel,Listbox,Label,Button,Grid,Scrollbar
from tkinter import Message as TkMessage
from united.wishmanager import WishManager
from united.message import Message
import logging

"""
Wish 管理員 的視窗
"""

class WishManagerToplevel:

    #建構子
    def __init__(self, master, gameboard):
        logging.basicConfig(level=logging.INFO)
        self.gameboard = gameboard
        self.region_name = gameboard.getPageParam()["region_name"]
        self.role_name = gameboard.getPageParam()["role_name"]
        self.wishManager = WishManager() #wish manager
        topWidth = 300
        topHeight = 400
        self.wishManagerToplevel = Toplevel(master)
        self.wishManagerToplevel.grab_set()
        self.wishManagerToplevel.focus_set()
        topPadx = master.winfo_rootx() + (master.winfo_width()/2) - (topWidth/2)
        topPady = master.winfo_rooty() + (master.winfo_height()/2) - (topHeight/2)
        self.wishManagerToplevel.geometry("%dx%d+%d+%d" % (topWidth, topHeight, topPadx, topPady))
        self.lbYBar = Scrollbar(self.wishManagerToplevel, orient="vertical")
        self.wishLB = Listbox(self.wishManagerToplevel, width=5, yscrollcommand=self.lbYBar.set)
        self.wishNameL = Label(self.wishManagerToplevel, text="No data")
        self.wishDescrptionM = TkMessage(self.wishManagerToplevel, text="No data")
        self.wishBriefM = TkMessage(self.wishManagerToplevel, text="No data")
        self.attachToRoleBtn = Button(self.wishManagerToplevel, text="Attach to Role", command=self.attachWishToRole)
        self.wishNameL.grid(row=0, column=0, sticky="news")
        self.wishDescrptionM.grid(row=1, column=0, sticky="news")
        self.wishBriefM.grid(row=2, column=0, sticky="news")
        self.wishLB.grid(row=0, column=1, rowspan=3, sticky="news")
        self.lbYBar.grid(row=0, column=2, rowspan=3, columnspan=1, sticky="ns")
        self.attachToRoleBtn.grid(row=3, column=0, columnspan=3, sticky="news")
        Grid.grid_rowconfigure(self.wishManagerToplevel, 0 ,weight=0)
        Grid.grid_rowconfigure(self.wishManagerToplevel, 1 ,weight=1)
        Grid.grid_rowconfigure(self.wishManagerToplevel, 2 ,weight=1)
        Grid.grid_rowconfigure(self.wishManagerToplevel, 3 ,weight=1)
        Grid.grid_columnconfigure(self.wishManagerToplevel, 0 ,weight=1)
        Grid.grid_columnconfigure(self.wishManagerToplevel, 1 ,weight=0)
        Grid.grid_columnconfigure(self.wishManagerToplevel, 2 ,weight=0)
        #讀取願望 到 Listbox
        self.wishManager.loadWish() 
        for key in self.wishManager.wish_dict.keys():
            self.wishLB.insert("end", key)
        self.wishLB.bind("<<ListboxSelect>>", self.wishLbSelected)
        self.lbYBar.config(command=self.wishLB.yview)

    #願望清單被選擇
    def wishLbSelected(self, event):
        key = self.wishLB.get(self.wishLB.curselection())
        curr_wish = self.wishManager.wish_dict[key]
        self.wishNameL.config(text=curr_wish.name)
        self.wishDescrptionM.config(text=curr_wish.description)
        self.wishBriefM.config(text=curr_wish.brief)
        
    #將所選的 願望 附加到角色上
    def attachWishToRole(self):
        if len(self.wishLB.curselection()) == 1: #選擇一個wish
            key = self.wishLB.get(self.wishLB.curselection())
            curr_wish = self.wishManager.wish_dict[key]
            req_m = Message("attach_dream", {"region_name":self.region_name,
                                            "role_name":self.role_name,
                                            "wish_name":curr_wish.name,
                                            "wish_desc":curr_wish.description,
                                            "wish_brief":curr_wish.brief,
                                            "dreamer_uuid":str(self.gameboard.loginPlayer.player_uuid)})
            res_m = self.gameboard.getClient().sendMessage(req_m)
            self.wishManagerToplevel.destroy()
        else:
            logging.warning("wish length of Listbox selection is not 1.")
            pass