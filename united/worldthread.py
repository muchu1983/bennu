"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import threading
import time
import logging
from http.server import HTTPServer
"""
World 更新 loop 每秒更新1次
"""
class WorldThread(threading.Thread):

    #建構子
    def __init__(self):
        threading.Thread.__init__(self) #Thread 子類別的建構子必須加這行
        self.isWorldRunning = False

    #覆寫 Thread 的 run 方法
    def run(self):
        try:
            self.isWorldRunning = True
            while(self.isWorldRunning == True):
                time.sleep(1)
        except:
            logging.error("World loop encounter exception!")
            self.shutdown()#停止 World loop
        else:
            self.shutdown()#停止 World loop
            
    #停止 World loop
    def shutdown(self):
        self.isWorldRunning = False