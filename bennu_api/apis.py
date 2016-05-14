# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
from bennu.localdb import LocalDbForCurrencyApi

#轉換貨幣
def exchangeCurrency(strDate=None, fMoney=0.0, strFrom="TWD", strTo="TWD"):
    db = LocalDbForCurrencyApi().mongodb
    fFromUSDRate = 0.0
    fToUSDRate = 0.0
    if strFrom == "USD":
        fFromUSDRate = 1.0
    else:
        docFromExRate = db.ex_rate.find_one({"strCurrencyName":"USD"+strFrom})
        fFromUSDRate = docFromExRate["fUSDollar"]
    if strTo == "USD":
        fToUSDRate = 1.0
    else:
        docToExRate = db.ex_rate.find_one({"strCurrencyName":"USD"+strTo})
        fToUSDRate = docToExRate["fUSDollar"]
    logging.info("exchange %f dollar from %s to %s"%(fMoney, strFrom, strTo))
    fResultMoney = (fMoney * fToUSDRate) / fFromUSDRate
    return fResultMoney
    
