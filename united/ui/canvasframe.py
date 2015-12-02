"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from tkinter import Frame,Canvas,Button,Label,Grid,Scrollbar,font
from tkinter import Message as TkMessage #名稱衝突
from united.message import Message
from PIL import Image,ImageTk

"""
遊戲進行中 的畫面頁
"""
class CanvasFrame:

    #構建子
    def __init__(self, master, gameboard):
        self.frame = Frame(master)
        self.board = gameboard
        self.preservedCanvasWidgetId = []
        self.loginedPlayerDataId = None
        #畫布區內容
        self.canvasXBar = Scrollbar(self.frame, orient="horizontal")
        self.canvasYBar = Scrollbar(self.frame, orient="vertical")
        self.worldCanvas = Canvas(self.frame, bg="blue", xscrollcommand=self.canvasXBar.set, yscrollcommand=self.canvasYBar.set)
        self.worldCanvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky="nwes")
        self.canvasXBar.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="ew")
        self.canvasYBar.grid(row=0, column=1, rowspan=4, columnspan=1, sticky="ns")
        self.canvasXBar.config(command=self.canvasXViewUpdate)
        self.canvasYBar.config(command=self.canvasYViewUpdate)
        #上右 地圖框內容
        mapFrame = Frame(self.frame, bg="green")
        mapFrame.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="news")
        #中右 描述框內容
        self.descriptionFrame = Frame(self.frame, bg="yellow")
        self.descriptionFrame.grid(row=1, column=2, rowspan=1, columnspan=1, sticky="news")
        #下右 命令框內容
        commandFrame = Frame(self.frame, bg="red")
        commandFrame.grid(row=2, column=2, rowspan=2, columnspan=1, sticky="news")
        # 分配 grid 的比重
        Grid.grid_rowconfigure(self.frame, 0, weight=1)
        Grid.grid_rowconfigure(self.frame, 1, weight=5)
        Grid.grid_rowconfigure(self.frame, 2, weight=2)
        Grid.grid_rowconfigure(self.frame, 3, weight=0)
        Grid.grid_columnconfigure(self.frame, 0, weight=10)
        Grid.grid_columnconfigure(self.frame, 1, weight=0)
        Grid.grid_columnconfigure(self.frame, 2, weight=1)

    #更新頁面資料 (區域的內容)
    def updatePageData(self):
        #先清除 (略過 preservedCanvasWidgetId 中的 item)
        for id in self.worldCanvas.find_withtag("all"):
            if id not in self.preservedCanvasWidgetId:
                self.worldCanvas.delete(id)
        #再重建
        self.currentWorldImg = ImageTk.PhotoImage(image=Image.open(os.getcwd() + "\\resource\\world.png"))
        self.worldCanvas.create_image(self.currentWorldImg.width()/2, self.currentWorldImg.height()/2, image=self.currentWorldImg)
        self.worldCanvas.config(scrollregion=(0, 0, self.currentWorldImg.width(), self.currentWorldImg.height())) #設定 canvas scroll XY bar 區域
        self.worldCanvas.create_polygon((10,10, 10,100, 100,100, 200,10, 200,200, 100,150, 10,150), fill="blue", activefill="green", stipple="gray12", activestipple="gray75", tag="area")
        self.worldCanvas.tag_bind("area", "<Button-1>", self.areaOnClick)
        #繪製登入者資訊(一次性)
        if self.loginedPlayerDataId not in self.preservedCanvasWidgetId:
            canvas_center_x = self.worldCanvas.winfo_width()/2
            cx = self.worldCanvas.canvasx(canvas_center_x)
            cy = self.worldCanvas.canvasy(10)
            self.loginedPlayerDataId = self.worldCanvas.create_text(cx, cy, font=font.Font(weight="bold"), fill="magenta")
            self.preservedCanvasWidgetId.append(self.loginedPlayerDataId)
        req_msg_3 = Message("get_logined_player", {"player_uuid":str(self.board.loginedPlayer.player_uuid)}) #取得登入玩家資料
        res_m_3 = self.board.getClient().sendMessage(req_msg_3)
        logined_player_name = res_m_3.getContents()["player_name"]
        logined_player_prestige = res_m_3.getContents()["player_prestige"]
        self.worldCanvas.itemconfig(self.loginedPlayerDataId, text="玩家:" + logined_player_name + " 聲望值:" + str(logined_player_prestige))
        self.worldCanvas.tag_raise(self.loginedPlayerDataId)
        
    def areaOnClick(self, event):
        id = event.widget.find_closest(event.x, event.y)
        print(event.widget.gettags(id))
        
    #canvas X 位移更新
    def canvasXViewUpdate(self, *args):
        self.worldCanvas.xview(*args)
        canvas_center_x = self.worldCanvas.winfo_width()/2
        cx = self.worldCanvas.canvasx(canvas_center_x)
        cy = self.worldCanvas.canvasy(10)
        self.worldCanvas.coords(self.loginedPlayerDataId, (cx, cy))
        
    #canvas Y 位移更新
    def canvasYViewUpdate(self, *args):
        self.worldCanvas.yview(*args)
        canvas_center_x = self.worldCanvas.winfo_width()/2
        cx = self.worldCanvas.canvasx(canvas_center_x)
        cy = self.worldCanvas.canvasy(10)
        self.worldCanvas.coords(self.loginedPlayerDataId, (cx, cy))
