"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
"""
訊息 物件 (以 json-rpc 傳遞)
"""
class Message:

    #建構子
    def __init__(self, title, contents):
        self.title = title
        self.contents = contents
        self.isValid() #首次自行檢查格式 (產生 self.valid)

    #檢查格式是否正確
    def isValid(self):
        self.valid = True
        if self.title is not None and self.contents is not None:
            if type(self.title) is not str: #title 須為 字串物件
                self.valid = False
            if type(self.contents) is not dict: #contents 須為 字典物件
                self.valid = False
            else:
                #contents 裡每個 key 須為 字串物件
                for key in self.contents.keys():
                    if type(key) is not str: 
                        self.valid = False
        else:
            self.valid = False
        return self.valid
    
    #編碼
    def encoding_to_json(self):
        ret = None
        if self.isValid():
            ret = json.dumps([self.getTitle(), self.getContents()])
        return ret
    
    #解碼
    def decoding_from_json(self, json_str):
        decode = json.loads(json_str)
        if len(decode) == 2:
            self.title = decode[0]
            self.contents = decode[1]
        if self.isValid() == True:
            return self
        else:
            return None

    #title 的 getter
    def getTitle(self):
        return self.title
    
    #contents 的 getter
    def getContents(self):
        return self.contents
