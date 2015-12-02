"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import threading
import time
import logging
import json
from http.server import HTTPServer
"""
包含一個 http server 監聽來自 client 的 json 命令
"""
class HttpServerThread(threading.Thread):

    #建構子
    def __init__(self, handler):
        threading.Thread.__init__(self) #Thread 子類別的建構子必須加這行
        #http server
        self.server_address = ('', 8000)
        self.httpd = HTTPServer(self.server_address, handler)

    #覆寫 Thread 的 run 方法
    def run(self):
        try:
            self.httpd.serve_forever()
        except:
            logging.error("HTTP server encounter exception!")
            self.httpd.shutdown()#停止 serve_forever() 的 loop
            self.httpd.server_close() #關閉連線
        else:
            self.httpd.shutdown()#停止 serve_forever() 的 loop
            self.httpd.server_close() #關閉連線
