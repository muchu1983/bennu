"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
"""
角色 類別
"""
class Role:

    #建構子
    def __init__(self, role_name, region_x, region_y):
        self.name = role_name
        self.region_x = region_x
        self.region_y = region_y
        self.dreamIdList = []
