"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from urllib import request,parse
from io import BytesIO
from PIL import Image
"""
靜態地圖 類別
"""
class StaticMap:

    #建構子
    def __init__(self):
        self.url_base = "http://maps.googleapis.com/maps/api/staticmap?"
    
    #產生 tkinter Image 地圖
    def generateMapImage(self, centerStr, zoomNum, sizeStr, scaleNum):
        params = parse.urlencode({"center":centerStr, "zoom":zoomNum, "size":sizeStr, "scale":scaleNum,
                                    "language":"zh-TW", "maptype":"terrain", "format":"png"})
        url = request.urlopen(self.url_base + params)
        buffer = BytesIO(url.read())
        image = Image.open(buffer)
        return image