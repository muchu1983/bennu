# -*- coding: utf-8 -*-
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import json
import urllib.request
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
    
#使用 Oauth 取得 facebook 使用者資料 return (id, name, email)
def getFacebookUserDataByOauth(strAuthCode=None):
    strFbClientId="1730077280596052"
    strFbClientSecret="23e738452f58c3c9de0a53e5c68c4c29"
    #交付 授權碼 給 Facebook 取得 access token
    strAccessTokenUrlTemplate = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s"
    strAccessTokenUrl = strAccessTokenUrlTemplate%(strFbClientId,
                                     "http://bennu-aws.ddns.net:5000/fb_oauth",
                                     strFbClientSecret,
                                     strAuthCode)
    responseToken = urllib.request.urlopen(strAccessTokenUrl)
    strToken =  responseToken.read().decode(responseToken.headers.get_content_charset())
    #以 access token 取得 使用者 資料
    responseUserData = urllib.request.urlopen("https://graph.facebook.com/me?fields=id,name,email&" + strToken)
    strUserData = responseUserData.read().decode(responseToken.headers.get_content_charset())
    dicUserData = json.loads(strUserData)
    return (dicUserData["id"], dicUserData["name"], dicUserData["email"])