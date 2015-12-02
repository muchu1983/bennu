"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import unittest
import logging
import time
from united.httpserverthread import HttpServerThread
from united.worldthread import WorldThread
from http.server import BaseHTTPRequestHandler

"""
測試 HTTP server
"""

class ServerThreadTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        
    #收尾
    def tearDown(self):
        self.httpThread = None
        self.worldThread = None

    #測試 啟動http server 2 秒後 關閉
    def test_start_http_server(self):
        logging.info("HttpServerThreadTest.test_start_http_server")
        self.httpThread = HttpServerThread(BaseHTTPRequestHandler)
        self.httpThread.start()
        time.sleep(2)
        self.httpThread.httpd.shutdown() #停止 serve_forever() 的 loop
        self.httpThread.httpd.server_close() #關閉連線
        
    #測試 啟動 world 主迴圈 2秒後 關閉
    def test_start_world_loop(self):
        self.worldThread = WorldThread()
        self.worldThread.start()
        time.sleep(2)
        self.worldThread.shutdown()

#測試開始
if __name__ == "__main__":
    unittest.main()


