# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import threading
import logging
from flask import Flask
from flask import request
from flask import jsonify
from bennu.api.spiderForYahooCurrency import SpiderForYahooCurrency
import bennu.api.apis as apis

app = Flask(__name__.split(".")[0])

#啟動 server
def start_flask_server():
    #啟動 spider 抓取 yahoo 網頁並更新匯率資料庫
    spider = SpiderForYahooCurrency()
    spiderThread = SpiderThread(spiderInstance=spider)
    spiderThread.start() #啟動執行緒
    #啟動 flask server
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    
#轉換貨幣至指定幣別 GET
@app.route("/ex_currency", methods=["GET"])
def exchangeCurrency():
    strDate = request.args.get("date", None, type=str) #歷史匯率(暫不處理)
    fMoney = request.args.get("money", 0.0, type=float) #金額
    strFromCurrency = request.args.get("from", "TWD", type=str).upper() #原始幣別
    strToCurrency = request.args.get("to", "TWD", type=str).upper() #目標幣別
    fResultMoney = apis.exchangeCurrency(fMoney=fMoney, strFrom=strFromCurrency, strTo=strToCurrency)
    return jsonify(fResultMoney=fResultMoney,
               form=strFromCurrency,
               to=strToCurrency)
               
#獨立執行 更新匯率資料庫 spider
class SpiderThread(threading.Thread):
    #thread 建構子
    def __init__(self, spiderInstance=None):
        threading.Thread.__init__(self) #初始化父層 Thread
        self.spider = spiderInstance
        
    #run
    def run(self):
        try:
            logging.info("SpiderThread running...")
            self.spider.runSpider()
        except Exception as ex:
            logging.warning("spider did not work.")
            logging.warning(ex)
        finally:
            logging.info("SpiderThread stoped.")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_flask_server()