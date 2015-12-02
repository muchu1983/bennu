"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from tkinter import Frame,Canvas,Button,Toplevel,Label,Entry,Text,Listbox,Grid,PhotoImage,Scrollbar
from tkinter import Message as TkMessage #名稱衝突
from PIL import Image,ImageTk
from united.emoji import Emoji
from united.message import Message
from united.role import Role
from united.ui.wishmanagertoplevel import WishManagerToplevel
from united.ui.createroledatatoplevel import CreateRoleDataToplevel
from united.ui.dreamviewertoplevel import DreamViewerToplevel
"""
遊戲進行中 的畫面頁
"""
class PlayFrame:

    #構建子
    def __init__(self, master, gameboard):
        self.frame = Frame(master)
        self.board = gameboard
        self.region_name = None
        self.role_name = None
        self.roleEmojiDict = {}
        self.activeRoleEmojiDict = {}
        self.updateCountdown = 10
        #中間畫布區內容
        self.canvasXBar = Scrollbar(self.frame, orient="horizontal")
        self.canvasYBar = Scrollbar(self.frame, orient="vertical")
        self.regionCanvas = Canvas(self.frame, bg="white", xscrollcommand=self.canvasXBar.set, yscrollcommand=self.canvasYBar.set)
        self.regionCanvas.grid(row=0, column=0, rowspan=1, columnspan=3, sticky="nwes")
        self.canvasXBar.grid(row=1, column=0, rowspan=1, columnspan=3, sticky="ew")
        self.canvasYBar.grid(row=0, column=3, rowspan=1, columnspan=1, sticky="ns")
        self.anchorLocationImg = PhotoImage(file=os.getcwd() + "\\resource\\loc.gif")
        center_x = self.regionCanvas.winfo_screenwidth()/2
        center_y = self.regionCanvas.winfo_screenheight()/2
        self.anchorLocationId = self.regionCanvas.create_image(center_x, center_y, image=self.anchorLocationImg, tags="anchor_location")
        self.loginedPlayerDataId = self.regionCanvas.create_text(center_x, center_y + 30)
        #下左 地圖框內容
        mapFrame = Frame(self.frame, bg="green")
        mapFrame.grid(row=2, column=0, columnspan=1, sticky="news")
        #下中 描述框內容
        self.descriptionFrame = Frame(self.frame, bg="yellow")
        self.descriptionFrame.grid(row=2, column=1, columnspan=1, sticky="news")
        self.defaultRoleImage = PhotoImage(file=os.getcwd() + "\\resource\\role.gif")
        self.roleImgL = Label(self.descriptionFrame, image=self.defaultRoleImage)
        self.roleDescM = TkMessage(self.descriptionFrame, text="description...")
        self.roleImgL.grid(row=0, column=0, sticky="news")
        self.roleDescM.grid(row=0, column=1, sticky="news")
        Grid.rowconfigure(self.descriptionFrame, 0, weight=1)
        Grid.columnconfigure(self.descriptionFrame, 0, weight=0)
        Grid.columnconfigure(self.descriptionFrame, 1, weight=1)
        #下右 命令框內容
        commandFrame = Frame(self.frame, bg="red")
        commandFrame.grid(row=2, column=2, columnspan=2, sticky="news")
        updateBtn = Button(commandFrame, text="update", command=self.updatePageData) #手動更新按鈕
        self.createRoleBtn = Button(commandFrame, text="建立角色", state="disable", command=self.createRoleDataToplevel) #建立角色 按鈕
        self.wishBtn = Button(commandFrame, text="托付願望", state="disable", command=self.createWishManagerToplevel) #設定願望 按鈕
        self.createRoleBtn.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.wishBtn.grid(row=0, column=1, padx=5, pady=5, sticky="news")
        updateBtn.grid(row=999, column=999)
        Grid.rowconfigure(commandFrame, 0, weight=1)
        Grid.columnconfigure(commandFrame, 0, weight=1)
        Grid.columnconfigure(commandFrame, 1, weight=1)
        # 分配 grid 的比重
        Grid.columnconfigure(self.frame, 0, weight=1)
        Grid.columnconfigure(self.frame, 1, weight=5)
        Grid.columnconfigure(self.frame, 2, weight=2)
        Grid.columnconfigure(self.frame, 3, weight=0)
        Grid.rowconfigure(self.frame, 0, weight=10)
        Grid.rowconfigure(self.frame, 1, weight=0)
        Grid.rowconfigure(self.frame, 2, weight=1)
        #bind event
        self.regionCanvas.bind("<Enter>", self.enter_regionCanvas)
        self.regionCanvas.bind("<Leave>", self.leave_regionCanvas)
        self.regionCanvas.bind("<Button-1>", self.mouseButton1Clicked)

    #更新頁面資料 (區域的內容)
    def updatePageData(self):
        #先清除 (略過部分 item)
        for id in self.regionCanvas.find_withtag("all"):
            if id != self.anchorLocationId and id != self.loginedPlayerDataId:
                self.regionCanvas.delete(id)
        #再重建
        self.region_name = self.board.getPageParam()["region_name"]
        req_msg_1 = Message("get_region_data", {"region_name":self.region_name})
        res_m_1 = self.board.getClient().sendMessage(req_msg_1)
        for i in range(len(res_m_1.getContents().keys())):
            role_name = res_m_1.getContents()[str(i)]
            req_msg_2 = Message("get_role_data", {"region_name":self.region_name, "role_name":role_name})
            res_m_2 = self.board.getClient().sendMessage(req_msg_2)
            region_x = res_m_2.getContents()["region_x"]
            region_y = res_m_2.getContents()["region_y"]
            dream_length = res_m_2.getContents()["dream_length"]
            display_txt = "%s(%d)" % (role_name, dream_length)
            self.regionCanvas.create_text(region_x, region_y-30, text=display_txt, tags=role_name)
            self.regionCanvas.create_image(region_x, region_y, image=self.getRoleEmojiPhotoImage(role_name, ":smile:"),
                                                                activeimage=self.getActiveRoleEmojiPhotoImage(role_name, ":smile:"))
        req_msg_3 = Message("get_logined_player", {"player_uuid":str(self.board.loginPlayer.player_uuid)})
        res_m_3 = self.board.getClient().sendMessage(req_msg_3) #送出 request
        logined_player_name = res_m_3.getContents()["player_name"]
        logined_player_prestige = res_m_3.getContents()["player_prestige"]
        self.regionCanvas.itemconfig(self.loginedPlayerDataId, text="玩家:" + logined_player_name + "\n聲望值:" + str(logined_player_prestige))
        self.regionCanvas.tag_raise(self.anchorLocationId)
        self.regionCanvas.tag_raise(self.loginedPlayerDataId)
        #設定 canvas scroll XY bar 區域
        allWidgetRegion = self.regionCanvas.bbox("all")
        expandedRegion = (0, 0, allWidgetRegion[2] + 1000, allWidgetRegion[3] + 1000)
        self.regionCanvas.config(scrollregion=expandedRegion)
        self.canvasXBar.config(command=self.regionCanvas.xview)
        self.canvasYBar.config(command=self.regionCanvas.yview)

    #取得角色 emoji 圖
    def getRoleEmojiPhotoImage(self, role_name, short_code):
        img = Image.open(Emoji(short_code).getImgPath()).resize((35,35), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(image=img)
        self.roleEmojiDict[role_name] = tkimg
        return tkimg
        
    #取得 active 狀態的 角色 emoji 圖 
    def getActiveRoleEmojiPhotoImage(self, role_name, short_code):
        img = Image.open(Emoji(short_code).getImgPath()).resize((45,45), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(image=img)
        self.activeRoleEmojiDict[role_name] = tkimg
        return tkimg
            
    # 設定錨點位置
    def mouseButton1Clicked(self, event):
        cx = self.regionCanvas.canvasx(event.x)
        cy = self.regionCanvas.canvasy(event.y)
        self.regionCanvas.coords(self.anchorLocationId, (cx, cy))
        self.regionCanvas.coords(self.loginedPlayerDataId, (cx, cy + 30))
        # 更新 description frame 內容
        req_m = Message("find_cloest_role", {"region_name":self.region_name, "region_x":cx, "region_y":cy})
        res_m = self.board.getClient().sendMessage(req_m) #送出 request
        if len(res_m.getContents().keys()) == 2:
            self.role_name = res_m.getContents()["role_name"]
            self.board.getPageParam()["role_name"] = self.role_name
            self.roleDescM.config(text=self.role_name)
            self.createRoleBtn.config(state="disable")
            self.wishBtn.config(state="active")
            dream_id_list = res_m.getContents()["dream_list"]
            if(len(dream_id_list) != 0):
                dreamViewerTop = DreamViewerToplevel(self.regionCanvas, self.board, dream_id_list)
        else:
            self.role_name = None
            self.roleDescM.config(text="")
            self.createRoleBtn.config(state="active")
            self.wishBtn.config(state="disable")
            
    #顯示 建立角色 視窗
    def createRoleDataToplevel(self):
        anchorLoc = self.regionCanvas.coords(self.anchorLocationId)
        rdTop = CreateRoleDataToplevel(self.regionCanvas, self.region_name, anchorLoc, self)

    #顯示 Wish Manager 視窗
    def createWishManagerToplevel(self):
        wmtop = WishManagerToplevel(self.regionCanvas, self.board)

    #滑鼠 進入 canvas
    def enter_regionCanvas(self, event):
        self.updateCountdown-=1
        if self.updateCountdown < 0:
            self.updatePageData()
            self.updateCountdown = 10

    #滑鼠 離開 canvas
    def leave_regionCanvas(self, event):
        pass
    
