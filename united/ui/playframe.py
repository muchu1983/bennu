"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
from tkinter import Frame,Canvas,Button,Toplevel,Label,Entry,Text,Listbox,Grid,Scrollbar,font
from tkinter import Message as TkMessage #名稱衝突
from PIL import Image,ImageTk
from united.emoji import Emoji
from united.message import Message
from united.role import Role
from united.staticmap import StaticMap
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
        self.dreamExclamationEmojiDict = {}
        self.preservedCanvasWidgetId = []
        self.updateCountdown = 100 #倒數為0時自動更新畫布
        #畫布區內容
        self.canvasXBar = Scrollbar(self.frame, orient="horizontal")
        self.canvasYBar = Scrollbar(self.frame, orient="vertical")
        self.regionCanvas = Canvas(self.frame, bg="blue", xscrollcommand=self.canvasXBar.set, yscrollcommand=self.canvasYBar.set)
        self.regionCanvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky="nwes")
        self.canvasXBar.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="ew")
        self.canvasYBar.grid(row=0, column=1, rowspan=4, columnspan=1, sticky="ns")
        self.regionCanvas.config(scrollregion=(0, 0, 1280, 1280)) #設定 canvas scroll XY bar 區域
        self.canvasXBar.config(command=self.canvasXViewUpdate)
        self.canvasYBar.config(command=self.canvasYViewUpdate)
        self.anchorLocationId = None
        self.loginedPlayerDataId = None
        self.backgroundImageId = None
        #上右 地圖框內容
        mapFrame = Frame(self.frame, bg="green")
        mapFrame.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="news")
        #中右 描述框內容
        self.descriptionFrame = Frame(self.frame, bg="yellow")
        self.descriptionFrame.grid(row=1, column=2, rowspan=1, columnspan=1, sticky="news")
        self.defaultRoleImage = Image.open(Emoji(":sunglasses:").getImgPath()).resize((50,80), Image.ANTIALIAS)
        self.defaultRoleTkimage = ImageTk.PhotoImage(image=self.defaultRoleImage)
        self.roleImgL = Label(self.descriptionFrame, image=self.defaultRoleTkimage)
        self.roleDescM = TkMessage(self.descriptionFrame, text="description...")
        self.roleImgL.grid(row=0, column=0, sticky="news")
        self.roleDescM.grid(row=1, column=0, sticky="news")
        Grid.rowconfigure(self.descriptionFrame, 0, weight=0)
        Grid.rowconfigure(self.descriptionFrame, 1, weight=1)
        Grid.columnconfigure(self.descriptionFrame, 0, weight=1)
        #下右 命令框內容
        commandFrame = Frame(self.frame, bg="red")
        commandFrame.grid(row=2, column=2, rowspan=2, columnspan=1, sticky="news")
        updateBtn = Button(commandFrame, text="手動更新", command=self.updatePageData)
        self.createRoleBtn = Button(commandFrame, text="建立角色", state="disable", command=self.createRoleDataToplevel) #建立角色 按鈕
        self.wishBtn = Button(commandFrame, text="托付願望", state="disable", command=self.createWishManagerToplevel) #設定願望 按鈕
        self.returnRegionBtn = Button(commandFrame, text="選擇區域", state="active", command=self.returnRegionPage) #返回區域選擇畫面 按鈕
        self.createRoleBtn.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self.wishBtn.grid(row=1, column=0, padx=5, pady=5, sticky="news")
        self.returnRegionBtn.grid(row=2, column=0, padx=5, pady=5, sticky="news")
        updateBtn.grid(row=3, column=0, padx=5, pady=5, sticky="news")
        Grid.rowconfigure(commandFrame, 0, weight=1)
        Grid.rowconfigure(commandFrame, 1, weight=1)
        Grid.rowconfigure(commandFrame, 2, weight=1)
        Grid.rowconfigure(commandFrame, 3, weight=0)
        Grid.columnconfigure(commandFrame, 0, weight=1)
        # 分配 grid 的比重
        Grid.grid_rowconfigure(self.frame, 0, weight=1)
        Grid.grid_rowconfigure(self.frame, 1, weight=5)
        Grid.grid_rowconfigure(self.frame, 2, weight=2)
        Grid.grid_rowconfigure(self.frame, 3, weight=0)
        Grid.grid_columnconfigure(self.frame, 0, weight=10)
        Grid.grid_columnconfigure(self.frame, 1, weight=0)
        Grid.grid_columnconfigure(self.frame, 2, weight=1)
        #bind event
        self.regionCanvas.bind("<Motion>", self.motion_regionCanvas)
        self.regionCanvas.bind("<Button-1>", self.mouseButton1Clicked)

    #更新頁面資料 (區域的內容)
    def updatePageData(self):
        #先清除 (略過部分 item)
        for id in self.regionCanvas.find_withtag("all"):
            if id not in self.preservedCanvasWidgetId:
                self.regionCanvas.delete(id)
        #再重建
        self.region_name = self.board.getPageParam()["region_name"]
        if self.backgroundImageId not in self.preservedCanvasWidgetId:#繪製背景地圖(一次性)
            map = StaticMap() 
            self.mapImg = map.generateMapImage(self.region_name, 12, "640x640", 2)
            self.mapTkimg = ImageTk.PhotoImage(image=self.mapImg)
            self.backgroundImageId = self.regionCanvas.create_image(640, 640, image=self.mapTkimg)
            self.preservedCanvasWidgetId.append(self.backgroundImageId)
        if self.loginedPlayerDataId not in self.preservedCanvasWidgetId:#繪製登入者資訊(一次性)
            canvas_center_x = self.regionCanvas.winfo_width()/2
            cx = self.regionCanvas.canvasx(canvas_center_x)
            cy = self.regionCanvas.canvasy(10)
            self.loginedPlayerDataId = self.regionCanvas.create_text(cx, cy, font=font.Font(weight="bold"), fill="magenta")
            self.preservedCanvasWidgetId.append(self.loginedPlayerDataId)
        if self.anchorLocationId not in self.preservedCanvasWidgetId:#繪製游標(一次性)
            canvas_center_x = self.regionCanvas.winfo_width()/2
            canvas_center_y = self.regionCanvas.winfo_height()/2
            self.anchorLocationImg = Image.open(Emoji(":triangular_flag_on_post:").getImgPath()).resize((35,35), Image.ANTIALIAS)
            self.anchorLocationTkimg = ImageTk.PhotoImage(image=self.anchorLocationImg)
            self.anchorLocationId = self.regionCanvas.create_image(canvas_center_x, canvas_center_y, image=self.anchorLocationTkimg, tags="anchor_location")
            self.preservedCanvasWidgetId.append(self.anchorLocationId)
        req_msg_1 = Message("get_region_data", {"region_name":self.region_name}) #取得角色(名稱)
        res_m_1 = self.board.getClient().sendMessage(req_msg_1)
        for i in range(len(res_m_1.getContents().keys())):
            role_name = res_m_1.getContents()[str(i)]
            req_msg_2 = Message("get_role_data", {"region_name":self.region_name, "role_name":role_name}) #取得角色(資料)
            res_m_2 = self.board.getClient().sendMessage(req_msg_2)
            region_x = res_m_2.getContents()["region_x"]
            region_y = res_m_2.getContents()["region_y"]
            dream_length = res_m_2.getContents()["dream_length"]
            self.regionCanvas.create_text(region_x, region_y-30, text=role_name, font=font.Font(weight="bold"), fill="magenta", tags=role_name)
            self.regionCanvas.create_image(region_x, region_y, image=self.getRoleEmojiPhotoImage(role_name, ":smile:"),
                                                                activeimage=self.getActiveRoleEmojiPhotoImage(role_name, ":smile:"))
            if dream_length > 0:
                self.regionCanvas.create_image(region_x+20, region_y-10, image=self.getDreamExclamationEmojiPhotoImage(role_name))
        req_msg_3 = Message("get_logined_player", {"player_uuid":str(self.board.loginPlayer.player_uuid)}) #取得登入玩家資料
        res_m_3 = self.board.getClient().sendMessage(req_msg_3)
        logined_player_name = res_m_3.getContents()["player_name"]
        logined_player_prestige = res_m_3.getContents()["player_prestige"]
        self.regionCanvas.itemconfig(self.loginedPlayerDataId, text="玩家:" + logined_player_name + " 聲望值:" + str(logined_player_prestige))
        self.regionCanvas.tag_raise(self.anchorLocationId)
        self.regionCanvas.tag_raise(self.loginedPlayerDataId)
        
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
        
    #取得 夢想驚嘆號 emoji 圖
    def getDreamExclamationEmojiPhotoImage(self, role_name):
        img = Image.open(Emoji(":exclamation:").getImgPath()).resize((20,20), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(image=img)
        self.dreamExclamationEmojiDict[role_name] = tkimg
        return tkimg
    
    # 設定錨點位置
    def mouseButton1Clicked(self, event):
        cx = self.regionCanvas.canvasx(event.x)
        cy = self.regionCanvas.canvasy(event.y)
        self.regionCanvas.coords(self.anchorLocationId, (cx, cy))
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
    
    #返回區域選擇畫面
    def returnRegionPage(self):
        self.preservedCanvasWidgetId = []
        self.board.setPageParam({})
        self.board.updatePageData("region_page")
        self.board.switchPage("region_page")

    #滑鼠在 canvas 中移動
    def motion_regionCanvas(self, event):
        self.updateCountdown-=1
        if self.updateCountdown < 0:
            self.updatePageData()
            self.updateCountdown = 100
    
    #canvas X 位移更新
    def canvasXViewUpdate(self, *args):
        self.regionCanvas.xview(*args)
        canvas_center_x = self.regionCanvas.winfo_width()/2
        cx = self.regionCanvas.canvasx(canvas_center_x)
        cy = self.regionCanvas.canvasy(10)
        self.regionCanvas.coords(self.loginedPlayerDataId, (cx, cy))
        
    #canvas Y 位移更新
    def canvasYViewUpdate(self, *args):
        self.regionCanvas.yview(*args)
        canvas_center_x = self.regionCanvas.winfo_width()/2
        cx = self.regionCanvas.canvasx(canvas_center_x)
        cy = self.regionCanvas.canvasy(10)
        self.regionCanvas.coords(self.loginedPlayerDataId, (cx, cy))
