# -*- coding: utf-8 -*-
"""
Copyright (C) 2016, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import logging
import smtplib
from email.mime.text import MIMEText

class EmailUtility:
    
    #建構子
    def __init__(self):
        #default email setting
        self.DEFAULT_SMTP = "smtp.gmail.com:587"
        self.DEFAULT_ACCOUNT = "public.muchu1983@gmail.com"
        self.DEFAULT_PASSWORD = "bee520BEE520"
        
    #寄送 email
    def sendEmail(self, strSubject=None, strFrom=None, strTo=None, strMsg=None, lstStrTarget=None, strSmtp=None, strAccount=None, strPassword=None):
        if not (strSmtp and strAccount and strPassword):
            strSmtp = self.DEFAULT_SMTP
            strAccount = self.DEFAULT_ACCOUNT
            strPassword = self.DEFAULT_PASSWORD
        #郵件內容
        msg = MIMEText(strMsg)
        msg["Subject"] = strSubject
        msg["From"] = strFrom
        msg["To"] = strTo
        #傳送
        server = smtplib.SMTP(strSmtp)
        server.ehlo()
        server.starttls()
        server.login(strAccount, strPassword)
        server.sendmail(strAccount, lstStrTarget, msg.as_string())
        server.quit()