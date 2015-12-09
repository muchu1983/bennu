"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import base64
import logging
import json
import tempfile
from tkinter import Frame,Canvas,Button,Label,Grid,Scrollbar,font,filedialog,StringVar
from tkinter import Message as TkMessage #名稱衝突
from united.message import Message
from united.emoji import Emoji
from united.ui.hyperlinktoplevel import HyperlinkToplevel
from PIL import Image,ImageTk

"""
遊戲進行中 的畫面頁
"""
class CanvasFrame:

    #構建子
    def __init__(self, master, gameboard):
        logging.basicConfig(level=logging.INFO)
        self.frame = Frame(master)
        self.board = gameboard
        self.preservedCanvasWidgetId = []
        self.loginedPlayerDataId = None
        self.currentLoadedUrlDataId = None
        self.currentLoadedImg = None
        self.currentLoadedUrl = None
        self.currentLoadedHyperlinkDescriptionDict = {}
        self.postNewImageButtonId = None
        self.rootUrl = "root" #首頁
        self.tempTag = "setting_hyperlink_area"
        #畫布區內容
        self.canvasXBar = Scrollbar(self.frame, orient="horizontal")
        self.canvasYBar = Scrollbar(self.frame, orient="vertical")
        self.worldCanvas = Canvas(self.frame, bg="blue", xscrollcommand=self.canvasXBar.set, yscrollcommand=self.canvasYBar.set)
        self.worldCanvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky="nwes")
        self.canvasXBar.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="ew")
        self.canvasYBar.grid(row=0, column=1, rowspan=4, columnspan=1, sticky="ns")
        self.canvasXBar.config(command=self.canvasXViewUpdate)
        self.canvasYBar.config(command=self.canvasYViewUpdate)
        #上右 位址框內容
        mapFrame = Frame(self.frame, bg="green")
        mapFrame.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="news")
        #中右 超連結描述框內容
        self.descriptionFrame = Frame(self.frame, bg="yellow")
        self.descriptionFrame.grid(row=1, column=2, rowspan=1, columnspan=1, sticky="news")
        self.hyperlinkNameVar = StringVar()
        self.hyperlinkDescVar = StringVar()
        hyperlinkNameL = Label(self.descriptionFrame, bg="yellow", textvariable=self.hyperlinkNameVar)
        hyperlinkDescTkM = TkMessage(self.descriptionFrame, anchor="nw", bg="white", textvariable=self.hyperlinkDescVar)
        hyperlinkNameL.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="news")
        hyperlinkDescTkM.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="news")
        Grid.grid_rowconfigure(self.descriptionFrame, 0, weight=0)
        Grid.grid_rowconfigure(self.descriptionFrame, 1, weight=1)
        Grid.grid_columnconfigure(self.descriptionFrame, 0, weight=1)
        #下右 命令框內容
        commandFrame = Frame(self.frame, bg="red")
        commandFrame.grid(row=2, column=2, rowspan=2, columnspan=1, sticky="news")
        setHyperlinkAreaBtn = Button(commandFrame, text="新增\n連結區塊", command=self.setHyperlinkArea)
        setHyperlinkAreaBtn.grid(row=0, column=0, rowspan=1, columnspan=1, padx=5, pady=5, sticky="news")
        Grid.grid_rowconfigure(commandFrame, 0, weight=1)
        Grid.grid_columnconfigure(commandFrame, 0, weight=1)
        # 分配 grid 的比重
        Grid.grid_rowconfigure(self.frame, 0, weight=1)
        Grid.grid_rowconfigure(self.frame, 1, weight=5)
        Grid.grid_rowconfigure(self.frame, 2, weight=2)
        Grid.grid_rowconfigure(self.frame, 3, weight=0)
        Grid.grid_columnconfigure(self.frame, 0, weight=10)
        Grid.grid_columnconfigure(self.frame, 1, weight=0)
        Grid.grid_columnconfigure(self.frame, 2, weight=1)
        
    # 由 screen (x,y) 轉換為 canvas (cx,cy)
    def convertXY2CXCY(self, x, y):
        cx = self.worldCanvas.canvasx(x)
        cy = self.worldCanvas.canvasy(y)
        return (cx, cy)
        
    #canvas X 位移更新
    def canvasXViewUpdate(self, *args):
        self.worldCanvas.xview(*args)
        canvas_center_x = self.worldCanvas.winfo_width()/2
        cxcy = self.convertXY2CXCY(canvas_center_x, 10)
        self.worldCanvas.coords(self.loginedPlayerDataId, cxcy) #位置保持在 (canvas_center, 10)
        cxcy = self.convertXY2CXCY(10, 10)
        self.worldCanvas.coords(self.currentLoadedUrlDataId, cxcy) #位置保持在(10, 10)
        
    #canvas Y 位移更新
    def canvasYViewUpdate(self, *args):
        self.worldCanvas.yview(*args)
        canvas_center_x = self.worldCanvas.winfo_width()/2
        cxcy = self.convertXY2CXCY(canvas_center_x, 10)
        self.worldCanvas.coords(self.loginedPlayerDataId, cxcy) #位置保持在 (canvas_center, 10)
        cxcy = self.convertXY2CXCY(10, 10)
        self.worldCanvas.coords(self.currentLoadedUrlDataId, cxcy) #位置保持在(10, 10)
        
    #清除畫布內容 (保留部分 item)
    def cleanWorldCanvas(self):
        for id in self.worldCanvas.find_withtag("all"):
            if id not in self.preservedCanvasWidgetId:
                self.worldCanvas.delete(id)

    #更新畫布資料
    def updatePageData(self):
        self.cleanWorldCanvas()#清理畫布
        #繪製登入者資訊(一次性)
        if self.loginedPlayerDataId not in self.preservedCanvasWidgetId:
            canvas_center_x = self.worldCanvas.winfo_width()/2
            cxcy = self.convertXY2CXCY(canvas_center_x, 10)
            self.loginedPlayerDataId = self.worldCanvas.create_text(cxcy, anchor="n", font=font.Font(weight="bold"), fill="magenta")
            self.preservedCanvasWidgetId.append(self.loginedPlayerDataId)
        req_m = Message("get_logined_player", {"player_uuid":str(self.board.loginedPlayer.player_uuid)}) #取得登入玩家資料
        res_m = self.board.getClient().sendMessage(req_m)
        logined_player_name = res_m.getContents()["player_name"]
        logined_player_prestige = res_m.getContents()["player_prestige"]
        self.worldCanvas.itemconfig(self.loginedPlayerDataId, text="玩家:" + logined_player_name + " 聲望值:" + str(logined_player_prestige))
        #讀取首頁 root 圖片
        if self.currentLoadedUrl == None: 
            self.loadUrlImage(self.rootUrl)
        
    #載入 url 圖片
    def loadUrlImage(self, url):
        if self.currentLoadedUrl != None: #清理前一個url的圖片
            self.cleanWorldCanvas()
        self.currentLoadedUrl = url
        self.currentLoadedHyperlinkDescriptionDict = {}
        req_m_1 = Message("load_image_data", {"url":self.currentLoadedUrl})
        res_m_1 = self.board.getClient().sendMessage(req_m_1)
        statusCode = res_m_1.getContents()["status"]
        if statusCode == 0: #有找到對應於 url 的 圖片資料
            ret_img_b64_data = res_m_1.getContents()["image_data"]
            ret_img_mode = res_m_1.getContents()["image_mode"]
            ret_img_size = res_m_1.getContents()["image_size"]
            tempRetImg = tempfile.TemporaryFile()
            tempRetImg.write(base64.b64decode(ret_img_b64_data.encode("utf-8")))
            ret_img = Image.open(tempRetImg)
            self.currentLoadedImg = ImageTk.PhotoImage(image=ret_img)
            self.worldCanvas.create_image(self.currentLoadedImg.width()/2, self.currentLoadedImg.height()/2, image=self.currentLoadedImg)
            self.worldCanvas.config(scrollregion=(0, 0, self.currentLoadedImg.width(), self.currentLoadedImg.height())) #設定 canvas scroll XY bar 區域
            #取得目前 url 下的所有 hyperlink 並繪製
            req_m_2 = Message("list_hyperlink_on_url", {"masterurl":self.currentLoadedUrl})
            res_m_2 = self.board.getClient().sendMessage(req_m_2) #送出 list_hyperlink_on_url
            hyperlinkList = res_m_2.getContents()["hyperlink_list"]
            for h in hyperlinkList:
                #h = ["hyperlink","json_coords","shape","description"]
                hyperlinkUrl = h[0]
                coords = json.loads(h[1])
                description = h[3]
                self.worldCanvas.create_rectangle((coords[0],coords[1],coords[2],coords[3]),
                                                    fill="blue", activefill="green",
                                                    stipple="gray12", activestipple="gray75",
                                                    tag=hyperlinkUrl)
                self.currentLoadedHyperlinkDescriptionDict[hyperlinkUrl] = description
                # bind 事件 到 hyperlink 區塊上
                self.worldCanvas.tag_bind(hyperlinkUrl, "<Button-1>", self.hyperlinkOnClick)
                self.worldCanvas.tag_bind(hyperlinkUrl, "<Double-Button-1>", self.hyperlinkOnDoubleClick)
                self.worldCanvas.tag_bind(hyperlinkUrl, "<Enter>", self.hand2Cursor)
                self.worldCanvas.tag_bind(hyperlinkUrl, "<Leave>", self.mouseLeaveHyperlinkArea)
        else: #找不到對應於 url 的 圖片資料
            self.folderImg = ImageTk.PhotoImage(file=Emoji(":file_folder:").getImgPath())
            self.openFolderImg = ImageTk.PhotoImage(file=Emoji(":open_file_folder:").getImgPath())
            self.postNewImageButtonId = self.worldCanvas.create_image(self.worldCanvas.winfo_width()/2, self.worldCanvas.winfo_height()/2, image=self.folderImg, activeimage=self.openFolderImg, tags="post_new_image_button")
            self.worldCanvas.tag_bind("post_new_image_button", "<Button-1>", self.postNewImage)
            self.worldCanvas.tag_bind("post_new_image_button", "<Enter>", self.hand2Cursor)
            self.worldCanvas.tag_bind("post_new_image_button", "<Leave>", self.defaultCursor)
        self.currentLoadedUrlDataId = self.worldCanvas.create_text(10, 10, text=self.currentLoadedUrl, anchor="nw", font=font.Font(weight="bold"), fill="magenta")
        self.worldCanvas.tag_raise(self.loginedPlayerDataId) #將被圖片蓋住的 使用者資料 移到最上層
        
    #新增圖片
    def postNewImage(self, event):
        if self.postNewImageButtonId != None: #從畫布移除新增圖片按鈕
            self.worldCanvas.delete(self.postNewImageButtonId)
            self.worldCanvas.config(cursor="") #滑鼠指標改回預設
        imgFileName = filedialog.askopenfilename(filetypes=(("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("GIF files", "*.gif")))
        source_img = Image.open(imgFileName)
        image_b64_data = base64.b64encode(open(imgFileName, "rb").read()).decode("utf-8")
        req_m = Message("post_image_data", {"url":self.currentLoadedUrl,
                                            "image_data":image_b64_data,
                                            "image_mode":source_img.mode,
                                            "image_size":source_img.size})
        res_m = self.board.getClient().sendMessage(req_m)
        self.loadUrlImage(self.currentLoadedUrl)
        
    #建立超連結區塊
    def setHyperlinkArea(self):
        areaid = self.worldCanvas.create_rectangle((0,0,50,50), fill="blue", activefill="green", stipple="gray12", activestipple="gray75", tag=self.tempTag)
        self.worldCanvas.bind("<Motion>", self.moveSettingHyperlinkArea) #偵測移動位置
        self.worldCanvas.bind("<Button-1>", self.anchorSettingHyperlinkArea) #以滑鼠右鍵定位
        
    #讓正建立中的 超連結區塊 隨滑鼠指標移動
    def moveSettingHyperlinkArea(self, event):
        (cx, cy) = self.convertXY2CXCY(event.x, event.y)
        areaid = self.worldCanvas.find_withtag(self.tempTag)
        self.worldCanvas.coords(areaid, (cx, cy, cx+50, cy+50))
        
    #已定位好 超連結區塊 開始輸入資料
    def anchorSettingHyperlinkArea(self, event):
        self.worldCanvas.unbind("<Motion>") #停止移動 超連結區塊
        self.worldCanvas.unbind("<Button-1>") #已定位好
        self.hyperlinkTop = HyperlinkToplevel(self.worldCanvas, self) #顯示 超連結資料輸入 Toplevel
        
    #建立超連結
    def createHyperlink(self, shape, hyperlinkUrl, description):
        self.worldCanvas.addtag_withtag(hyperlinkUrl, self.tempTag) #改變 tag 為 hyperlink
        self.worldCanvas.dtag(hyperlinkUrl, self.tempTag) #移除 原有的 tag
        hyperlinkCoords = self.worldCanvas.bbox(hyperlinkUrl)
        hyperlinkData=(hyperlinkUrl,
              self.currentLoadedUrl,
              shape,
              hyperlinkCoords,
              description)
        logging.info(hyperlinkData)
        req_m = Message("create_hyperlink", {"hyperlink":hyperlinkUrl,
                                             "masterurl":self.currentLoadedUrl,
                                             "json_coords":json.dumps(hyperlinkCoords),
                                             "shape":shape,
                                             "description":description})
        res_m = self.board.getClient().sendMessage(req_m) #送出 create_hyperlink
        # bind 事件 到 hyperlink 區塊上
        self.worldCanvas.tag_bind(hyperlinkUrl, "<Button-1>", self.hyperlinkOnClick)
        self.worldCanvas.tag_bind(hyperlinkUrl, "<Double-Button-1>", self.hyperlinkOnDoubleClick)
        self.worldCanvas.tag_bind(hyperlinkUrl, "<Enter>", self.hand2Cursor)
        self.worldCanvas.tag_bind(hyperlinkUrl, "<Leave>", self.mouseLeaveHyperlinkArea)
        #紀錄超連結描述資料
        self.currentLoadedHyperlinkDescriptionDict[hyperlinkUrl] = description
        
    #點擊超連結
    def hyperlinkOnClick(self, event):
        (cx, cy) = self.convertXY2CXCY(event.x, event.y)
        id = event.widget.find_closest(cx, cy)
        tags = event.widget.gettags(id)
        self.hyperlinkNameVar.set(tags[0])
        self.hyperlinkDescVar.set(self.currentLoadedHyperlinkDescriptionDict[tags[0]])
        
    #滑鼠離開超連結區塊
    def mouseLeaveHyperlinkArea(self, event):
        self.worldCanvas.config(cursor="")
        self.hyperlinkNameVar.set("")
        self.hyperlinkDescVar.set("")
        
    #雙擊 超連結
    def hyperlinkOnDoubleClick(self, event):
        (cx, cy) = self.convertXY2CXCY(event.x, event.y)
        id = event.widget.find_closest(cx, cy)
        nextLoadedUrl = event.widget.gettags(id)[0]
        self.loadUrlImage(nextLoadedUrl)
        
    #滑鼠指標改為 手型
    def hand2Cursor(self, event):
        self.worldCanvas.config(cursor="hand2")
    
    #滑鼠指標改為 預設
    def defaultCursor(self, event):
        self.worldCanvas.config(cursor="")
