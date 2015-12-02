"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""

import base64
import uuid
from united.message import Message
from united.lockedcase import LockedCase

"""
圖塊超連結 模組
"""
class HyperlinkMod:

    #構構子
    def __init__(self):
        pass
        
    def dispatchMessage(self, message):
        message_title = message.getTitle()
        res_message = None
        if message_title == "create_hyperlink":
            pass
        elif: message_title == "list_hyperlink_on_url":
            pass
        return res_message
        
