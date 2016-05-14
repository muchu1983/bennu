# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import bennu.api.flaskrunner as flaskrunner

def entry_point():
    #logging 層級設定
    logging.basicConfig(level=logging.INFO)
    #啟動 flask http service (port 5000)
    flaskrunner.start_flask_server()

if __name__ == "__main__":
    entry_point()