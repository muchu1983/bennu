"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from united.localdb import SQLite3Db
from united.wish import Wish
"""
願望管理者 類別
"""

class WishManager:

    #建構子
    def __init__(self):
        self.wish_dict = {}
        self.db = SQLite3Db()
        
    #解構子
    def __del__(self):
        self.db = None #主動讓 db 被 garbage collection

    #加入願望
    def addWish(self, w_name, w_desc, w_brief):
        table = "wish"
        id = None #db.py 將 None 轉為 null
        data = [id, w_name, w_desc, w_brief]
        self.db.insertOne(table, data)
        
    #讀取願震
    def loadWish(self):
        table = "wish"
        wish_data = self.db.selectAll(table)
        self.wish_dict.clear() #先清除
        for wd in wish_data:
            self.wish_dict[str(wd[0])] = Wish(wd[0], wd[1], wd[2], wd[3])