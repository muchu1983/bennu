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
from http.server import BaseHTTPRequestHandler

"""
測試 HTTP server
"""

class HttpServerThreadTest(unittest.TestCase):

    #準備
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.httpserver = HttpServerThread(BaseHTTPRequestHandler)
        
    #收尾
    def tearDown(self):
        self.httpserver = None

    #測試 啟動http server 5 秒後 關閉
    def test_start_http_server(self):
        logging.info("HttpServerThreadTest.test_start_http_server")
        self.httpserver.start()
        time.sleep(5)
        self.httpserver.httpd.shutdown() #停止 serve_forever() 的 loop
        self.httpserver.httpd.server_close() #關閉連線


#測試開始
if __name__ == "__main__":
    unittest.main()


