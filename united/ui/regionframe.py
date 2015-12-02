"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from tkinter import Frame,Button,Grid
from united.message import Message
from functools import partial
"""
選擇 區域 頁面
"""

class RegionFrame:

    #建構子
    def __init__(self, master, gameboard):
        self.frame = Frame(master, bg="yellow")
        self.board = gameboard
        self.updateBtn = Button(self.frame, text="update", command=self.updatePageData)
        self.updateBtn.grid(row=999, column=999) # update button 暫放 右下角

    #切換到遊戲頁
    def switchToPlayPage(self, region_name):
        self.board.getPageParam()["region_name"] = region_name
        self.board.updatePageData("play_page")
        self.board.switchPage("play_page")

    #更新 區域 頁面 (列出 server world 上的所有Region )
    def updatePageData(self):
        #先清除widget (保留 update 按鈕)
        for widget in self.frame.winfo_children():
            if widget is not self.updateBtn:
                widget.destroy()
        #再重建
        req_m = Message("list_all_region", {"empty_contents":0})
        res_m = self.board.getClient().sendMessage(req_m)
        region_dict = res_m.getContents()
        max_column = 5
        curr_row = 0
        curr_column = 0
        Grid.rowconfigure(self.frame, 0, weight=1)
        for key in region_dict.keys():
            region_name = region_dict[key]
            btn = Button(self.frame, text=region_name, command=partial(self.switchToPlayPage, region_name))
            btn.grid(row=curr_row, column=curr_column, padx=5, pady=5, sticky="news")
            curr_column+=1
            if curr_column >= max_column:
                curr_row+=1
                curr_column = 0
                Grid.rowconfigure(self.frame, curr_row, weight=1)
        for i in range(max_column):
            Grid.columnconfigure(self.frame, i, weight=1)
        
