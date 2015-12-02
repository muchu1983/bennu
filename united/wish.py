"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
"""
願望 類別
"""

class Wish:

    #建構子
    def __init__(self, id, wish_name, description, brief_target):
        self.id = id
        self.name = wish_name
        self.description = description
        self.brief = brief_target
        
        