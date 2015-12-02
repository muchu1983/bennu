"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import math
from united.role import Role
"""
地區 類別
"""
class Region:

    #建構子
    def __init__(self, region_name):
        self.name = region_name
        self.role = []
        self.maxFindingRange = 20 #findCloestRole()依據

    #在區域加入角色
    def addRole(self, role_name, region_x, region_y):
        self.role.append(Role(role_name, region_x, region_y))

    #找出最靠近的角色
    def findCloestRole(self, req_x, req_y):
        targetRole = None
        findedMinRange = None
        for ro in self.role:
            dx = req_x - ro.region_x
            dy = req_y - ro.region_y
            distence = math.hypot(dx, dy) # sqrt(dx^2 + dy^2)
            if distence <= self.maxFindingRange: #在偵測範圍內
                if findedMinRange == None: #首次發現
                    findedMinRange = distence
                    targetRole = ro
                else:
                    if distence < findedMinRange: #取代上一個發現
                        findedMinRange = distence
                        targetRole = ro
        return targetRole
