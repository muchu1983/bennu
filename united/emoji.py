"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import re
import os
from tkinter import PhotoImage
"""
顏文字 物件
"""
class Emoji:
    
    #建構子
    def __init__(self, short_code):
        self.shortCode = short_code
        self.pattern = re.compile(":([a-z0-9\+\-_]+):")
        self.emoji_list = ["smile"]
        
    #取得圖片路徑
    def getImgPath(self):
        m = self.pattern.match(self.shortCode)
        if m == None: return None
        name = m.group(1)
        if name not in self.emoji_list: return None
        imgPath = os.getcwd() + "\\resource\\emoji\\" + name + ".png"
        return imgPath
        