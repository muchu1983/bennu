"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
from united.staticmap import StaticMap
from tkinter import Tk,Grid,Label
from PIL import Image,ImageTk

"""
測試 靜態地圖 類別
"""

class StaticMapTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        pass
        
    #收尾
    def tearDown(self):
        pass

    #測試 產生 tkinter Image 地圖
    def test_generateMapImage(self):
        logging.info("StaticMapTest.test_generateMapPhotoImage")
        root = Tk()
        map = StaticMap()
        mapImg = map.generateMapImage("文和街,台南市", 14, "640x640", 1)
        mapTkimg = ImageTk.PhotoImage(image=mapImg)
        l = Label(root, bg="green", image=mapTkimg)
        l.grid(row=0, column=0, sticky="news")
        Grid.grid_rowconfigure(root, 0, weight=1)
        Grid.grid_columnconfigure(root, 0, weight=1)
        root.mainloop()


#測試開始
if __name__ == "__main__":
    unittest.main(exit=False)


