"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import os
import base64
from tkinter import Frame,Canvas,Button,Label,Grid,Scrollbar,font,filedialog
from tkinter import Message as TkMessage #名稱衝突
from united.message import Message
from united.emoji import Emoji
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
        self.currentLoadedImg = None
        self.currentLoadedUrl = None
        self.postNewImageButtonId = None
        self.rootUrl = "root" #首頁
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
        
    #清除畫布內容 (保留部分 item)
    def cleanWorldCanvas(self):
        for id in self.worldCanvas.find_withtag("all"):
            if id not in self.preservedCanvasWidgetId:
                self.worldCanvas.delete(id)

    #更新畫布資料
    def updatePageData(self):
        self.cleanWorldCanvas()#清理畫布
        if self.currentLoadedUrl == None: #讀取首頁 root 圖片
            self.loadUrlImage(self.rootUrl)
        #繪製登入者資訊(一次性)
        if self.loginedPlayerDataId not in self.preservedCanvasWidgetId:
            canvas_center_x = self.worldCanvas.winfo_width()/2
            cx = self.worldCanvas.canvasx(canvas_center_x)
            cy = self.worldCanvas.canvasy(10)
            self.loginedPlayerDataId = self.worldCanvas.create_text(cx, cy, font=font.Font(weight="bold"), fill="magenta")
            self.preservedCanvasWidgetId.append(self.loginedPlayerDataId)
        req_m = Message("get_logined_player", {"player_uuid":str(self.board.loginedPlayer.player_uuid)}) #取得登入玩家資料
        res_m = self.board.getClient().sendMessage(req_m)
        logined_player_name = res_m.getContents()["player_name"]
        logined_player_prestige = res_m.getContents()["player_prestige"]
        self.worldCanvas.itemconfig(self.loginedPlayerDataId, text="玩家:" + logined_player_name + " 聲望值:" + str(logined_player_prestige))
        self.worldCanvas.tag_raise(self.loginedPlayerDataId)
        
    #載入 url 圖片
    def loadUrlImage(self, url):
        if self.currentLoadedUrl != None: #清理前一個url的圖片
            self.cleanWorldCanvas()
        self.currentLoadedUrl = url
        req_m = Message("load_image_data", {"url":url})
        res_m = self.board.getClient().sendMessage(req_m)
        statusCode = res_m.getContents()["status"]
        if statusCode == 0: #有找到對應於 url 的 圖片資料
            ret_img_b64_data = res_m.getContents()["image_data"]
            ret_img_mode = res_m.getContents()["image_mode"]
            ret_img_size = res_m.getContents()["image_size"]
            ret_img = Image.frombytes(ret_img_mode, ret_img_size, base64.b64decode(ret_img_b64_data.encode("utf-8")))
            self.currentLoadedImg = ImageTk.PhotoImage(image=ret_img)
            self.worldCanvas.create_image(self.currentLoadedImg.width()/2, self.currentLoadedImg.height()/2, image=self.currentLoadedImg)
            self.worldCanvas.config(scrollregion=(0, 0, self.currentLoadedImg.width(), self.currentLoadedImg.height())) #設定 canvas scroll XY bar 區域
            #取得hyperlink並繪製
            #self.worldCanvas.create_polygon((10,10, 10,100, 100,100, 200,10, 200,200, 100,150, 10,150), fill="blue", activefill="green", stipple="gray12", activestipple="gray75", tag="area")
            #self.worldCanvas.tag_bind("area", "<Button-1>", self.hyperlinkOnClick)
        else: #找不到對應於 url 的 圖片資料
            self.folderImg = ImageTk.PhotoImage(file=Emoji(":file_folder:").getImgPath())
            self.openFolderImg = ImageTk.PhotoImage(file=Emoji(":open_file_folder:").getImgPath())
            self.postNewImageButtonId = self.worldCanvas.create_image(self.worldCanvas.winfo_width()/2, self.worldCanvas.winfo_height()/2, image=self.folderImg, activeimage=self.openFolderImg, tags="post_new_image_button")
            self.worldCanvas.tag_bind("post_new_image_button", "<Button-1>", self.postNewImage)
            self.worldCanvas.tag_bind("post_new_image_button", "<Enter>", self.hand2Cursor)
            self.worldCanvas.tag_bind("post_new_image_button", "<Leave>", self.defaultCursor)
        
    #新增圖片
    def postNewImage(self, event):
        if self.postNewImageButtonId != None: #從畫布移除新增圖片按鈕
            self.worldCanvas.delete(self.postNewImageButtonId)
            self.worldCanvas.config(cursor="") #滑鼠指標改回預設
        imgFileName = filedialog.askopenfilename(filetypes=(("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("GIF files", "*.gif")))
        source_img = Image.open(imgFileName)
        image_b64_data = base64.b64encode(source_img.tobytes()).decode("utf-8")
        req_m = Message("post_image_data", {"url":self.currentLoadedUrl,
                                            "image_data":image_b64_data,
                                            "image_mode":source_img.mode,
                                            "image_size":source_img.size})
        res_m = self.board.getClient().sendMessage(req_m)
        self.loadUrlImage(self.currentLoadedUrl)
        
    #點擊超連結
    def hyperlinkOnClick(self, event):
        id = event.widget.find_closest(event.x, event.y)
        print(event.widget.gettags(id))
        
    #滑鼠指標改為 手型
    def hand2Cursor(self, event):
        self.worldCanvas.config(cursor="hand2")
    
    #滑鼠指標改為 預設
    def defaultCursor(self, event):
        self.worldCanvas.config(cursor="")
