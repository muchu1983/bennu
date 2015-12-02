"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import json
import logging
import base64
import uuid
from http.server import BaseHTTPRequestHandler
from united.message import Message
from united.lockedcase import LockedCase
"""
自定義 HTTP Request handler
"""

class JsonRequestHandler(BaseHTTPRequestHandler):
    #從world 讀取資訊再回覆給 client (唯讀用法)
    instanceOfWorld_read_only = None # class 靜態變數,server 啟動前設置為 world 實例物件
    # do_Get 測試用
    def do_GET(self):
        print("someone get in!")
        self.send_response(400) #狀態碼 400
    
    #覆寫 do_POST
    def do_POST(self):
        post_raw = self.rfile.read(int(self.headers.get("Content-Length"))) #bytes
        post_data = post_raw.decode("utf-8") # bytes to str
        post_message = Message(None, None).decoding_from_json(post_data)
        message_title = post_message.getTitle()
        if message_title == "just_for_test":
            #僅供測試使用
            ans_message = self.justfortest(post_message)
            self.sendResponseJsonMessage(200, ans_message) #狀態碼 200 -> 成功
        elif message_title == "get_region_data":
            #取得 region 的資料
            res_message = self.getRegionData(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "get_role_data":
            #取得 role 的資料
            res_message = self.getRoleData(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "list_all_region":
            #列出所有 region
            res_message = self.listAllRegion(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "create_new_role":
            #建立新的 role
            res_message = self.createNewRole(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "find_cloest_role":
            #找出最靠近的 role
            res_message = self.findCloestRole(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "create_player_account":
            #建立新的玩家帳號
            res_message = self.createPlayerAccount(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "player_account_login":
            #帳號登入取得UUID
            res_message = self.playerAccountLogin(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "attach_dream":
            #起心動念
            res_message = self.playerAttachDream(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "make_a_promise":
            #許下諾言
            res_message = self.playerMakeAPromise(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "abort_dream_promise":
            #放棄任務
            res_message = self.playerAbortDreamPromise(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "dream_come_true":
            #美夢成真
            res_message = self.playerDreamComeTrue(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "award_winning":
            #贏取獎勵
            res_message = self.playerAwardWinning(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "get_dream_data":
            #取得夢想資料以檢視
            res_message = self.getDreamData(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        elif message_title == "get_logined_player":
            #取得登入玩家資料
            res_message = self.getLoginedPlayer(post_message)
            self.sendResponseJsonMessage(200, res_message) #狀態碼 200 -> 成功
        else:
            #未定義的 message
            logging.error("Err: Undefined message.")
            res_message = Message("Undefined message.", {})
            self.sendResponseJsonMessage(400, res_message) # 狀態碼 400 -> 失敗
            
    # 將準備好的 message 物件解碼為 json 並回傳給 client
    def sendResponseJsonMessage(self, status_code, res_message):
        self.send_response(status_code) #狀態碼
        self.send_header("Content-type", "application/json; charset=utf-8") #header
        self.end_headers() #結束 headers 內容
        res_data = res_message.encoding_to_json() # message -> json(str)
        res_raw = res_data.encode('utf-8') # json(str) -> json(bytes)
        self.wfile.write(res_raw) #回覆 bytes 內容

    # test 1+1=2 (server 端透過 message 進行運算)
    def justfortest(self, message):
        """
            收到的 message 格式
            title = "just_for_test"
            contents = {"n1":1, "n2":1}
            回傳的 message 格式
            title = "just_for_test"
            contents = {"ans":2}
        """
        n1 = message.getContents()["n1"]
        n2 = message.getContents()["n2"]
        ans = n1 + n2
        ans_message = Message("just_for_test", {"ans":ans})
        return ans_message

    # 取得 region 的資料
    def getRegionData(self, message):
        """
            收到的 message 格式
            title = "get_region_data"
            contents = {"region_name":"xxxxxx"}
            回傳的 message 格式
            title = "get_region_data"
            contents = {"0":"aaaaaa","1":"bbbbbbb",...}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        request_region_name = message.getContents()["region_name"]
        role_name_dict = {}
        for re in world.region:
            if re.name == request_region_name:
                i = 0
                for ro in re.role:
                    role_name_dict[str(i)] = ro.name
                    i+=1
                break
        res_m = Message("get_region_data", role_name_dict)
        return res_m

    # 取得 role 的資料
    def getRoleData(self, message):
        """
            收到的 message 格式
            title = "get_role_data"
            contents = {"region_name":"xxxxxx", "role_name":"oooooo"}
            回傳的 message 格式
            title = "get_role_data"
            contents = {"name":"oooooooo", "region_x":100, "region_y":100, "dream_length":0}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        request_region_name = message.getContents()["region_name"]
        request_role_name = message.getContents()["role_name"]
        role_data = {}
        for re in world.region:
            if re.name == request_region_name:
                for ro in re.role:
                    if ro.name == request_role_name:
                        role_data["name"] = ro.name
                        role_data["region_x"] = ro.region_x
                        role_data["region_y"] = ro.region_y
                        role_data["dream_length"] = len(ro.dreamIdList)
        res_m = Message("get_role_data", role_data)
        return res_m

    #列出所有 region
    def listAllRegion(self, message):
        """
            收到的 message 格式
            title = "list_all_region"
            contents = {"empty_contents":0}
            回傳的 message 格式
            title = "list_all_region"
            contents = {"0":"aaaaaa", "1":"bbbbbbb",...}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        region_list = {}
        i = 0
        for re in world.region:
            region_list[str(i)] = re.name
            i+=1
        res_m = Message("list_all_region", region_list)
        return res_m

    # 建立新的 role (放入帶鎖箱)
    def createNewRole(self, message):
        """
            收到的 message 格式
            title = "create_new_role"
            contents = {"region_name":"xxx", "role_name":"ooo", "region_x":300, "region_y":200}
            回傳的 message 格式
            title = "create_new_role"
            contents = {"status":0}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        case = LockedCase()
        region_name = message.getContents()["region_name"]
        role_name = message.getContents()["role_name"]
        region_x = message.getContents()["region_x"]
        region_y = message.getContents()["region_y"]
        case.createNewRole(world, region_name, role_name, region_x, region_y)
        res_m = Message("create_new_role", {"status":0})
        return res_m

    #找出最靠近的 role
    def findCloestRole(self, message):
        """
            收到的 message 格式
            title = "find_cloest_role"
            contents = {"region_name":"xxxxx", "region_x":123, "region_y":321}
            回傳的 message 格式
            title = "find_cloest_role"
            contents = {"role_name":"role_name", "dream_list":["aaa-aaa","bbb-bbb-b"]}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        region_name = message.getContents()["region_name"]
        region_x = message.getContents()["region_x"]
        region_y = message.getContents()["region_y"]
        target_role = None
        for re in world.region:
            if re.name == region_name:
                target_role = re.findCloestRole(region_x, region_y)
                break
        res_m = None
        if target_role == None:
            res_m = Message("find_cloest_role", {})
        else:
            res_m = Message("find_cloest_role", {"role_name":target_role.name,
                            "dream_list":target_role.dreamIdList})
        return res_m
        
    #建立新的玩家帳號
    def createPlayerAccount(self, message):
        """
            收到的 message 格式
            title = "create_player_account"
            contents = {"player_account":"xxxxxx", "player_hashed_password":"b64xxxxxxxx"}
            回傳的 message 格式
            title = "create_player_account"
            contents = {"status":0}
        """
        case = LockedCase()
        player_acc = message.getContents()["player_account"]
        encoded_hashed = message.getContents()["player_hashed_password"]
        hashed = base64.b64decode(encoded_hashed.encode("utf-8"))
        player_uuid = uuid.uuid1()
        status_code = case.createPlayerAccount(player_uuid, player_acc, hashed) #建立帳號完成
        ret_m = Message("create_player_account", {"status":status_code})
        return ret_m
    
    #帳號登入取得UUID
    def playerAccountLogin(self, message):
        """
            收到的 message 格式
            title = "player_account_login"
            contents = {"player_account":"xxxxxx", "player_trans_password":"b64xxxxxxxxx"}
            回傳的 message 格式
            title = "player_account_login"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
        """
        case = LockedCase()
        player_acc = message.getContents()["player_account"]
        tran_pw = message.getContents()["player_trans_password"]
        player_uuid = case.accountLoginValidate(player_acc, tran_pw) #登入取得 uuid
        if player_uuid == None:
            ret_m = Message("player_account_login", {})
        else:
            ret_m = Message("player_account_login", {"player_uuid":str(player_uuid)})
        return ret_m
        
    #起心動念
    def playerAttachDream(self, message):
        """
            收到的 message 格式
            title = "attach_dream"
            contents = {"region_name":"xxx",
                            "role_name":"ooo",
                            "wish_name":"dddd",
                            "wish_desc":"xxxxx",
                            "wish_brief":"bbbb",
                            "dreamer_uuid":"uuuu-uuuu-uu"}
            回傳的 message 格式
            title = "attach_dream"
            contents = {"status":0}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        case = LockedCase()
        region_name = message.getContents()["region_name"]
        role_name = message.getContents()["role_name"]
        wish_name = message.getContents()["wish_name"]
        wish_desc = message.getContents()["wish_desc"]
        wish_brief = message.getContents()["wish_brief"]
        dreamer_uuid = message.getContents()["dreamer_uuid"]
        status_code = case.attachDreamToRole(world, region_name, role_name, wish_name, wish_desc, wish_brief, dreamer_uuid)
        ret_m = Message("attach_dream", {"status":status_code})
        return ret_m
        
    #許下諾言
    def playerMakeAPromise(self, message):
        """
            收到的 message 格式
            title = "make_a_promise"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd",
                        "realizer_uuid":"rrrr-rrrr-rrrr"}
            回傳的 message 格式
            title = "make_a_promise"
            contents = {"status":0}
        """
        case = LockedCase()
        dream_uuid = message.getContents()["dream_uuid"]
        realizer_uuid = message.getContents()["realizer_uuid"]
        status_code = case.realizerMakeAPromise(dream_uuid, realizer_uuid)
        ret_m = Message("make_a_promise", {"status":status_code})
        return ret_m
        
    #放棄任務
    def playerAbortDreamPromise(self, message):
        """
            收到的 message 格式
            title = "abort_dream_promise"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd",
                        "realizer_uuid":"rrrr-rrrr-rrrr"}
            回傳的 message 格式
            title = "abort_dream_promise"
            contents = {"status":0}
        """
        case = LockedCase()
        dream_uuid = message.getContents()["dream_uuid"]
        realizer_uuid = message.getContents()["realizer_uuid"]
        status_code = case.realizerAbortDreamPromise(dream_uuid, realizer_uuid)
        ret_m = Message("abort_dream_promise", {"status":status_code})
        return ret_m
    
    #美夢成真
    def playerDreamComeTrue(self, message):
        """
            收到的 message 格式
            title = "dream_come_true"
            contents = {"dream_uuid":"ddddd-dddd-dddddd",
                        "dreamer_uuid":"uuuu-uuuuu-uuu"}
            回傳的 message 格式
            title = "dream_come_true"
            contents = {"status":0}
        """
        case = LockedCase()
        dream_uuid = message.getContents()["dream_uuid"]
        dreamer_uuid = message.getContents()["dreamer_uuid"]
        status_code = case.dreamerDreamComeTrue(dream_uuid, dreamer_uuid)
        ret_m = Message("dream_come_true", {"status":status_code})
        return ret_m
        
    #贏取獎勵
    def playerAwardWinning(self, message):
        """
            收到的 message 格式
            title = "award_winning"
            contents = {"dream_uuid":"ddddd-dddd-dddddd",
                        "realizer_uuid":"rrrrr-rrrr-rrrrr"}
            回傳的 message 格式
            title = "award_winning"
            contents = {"status":0}
        """
        world = JsonRequestHandler.instanceOfWorld_read_only  #縮短變數名稱
        case = LockedCase()
        dream_uuid = message.getContents()["dream_uuid"]
        realizer_uuid = message.getContents()["realizer_uuid"]
        status_code = case.realizerAwardWinning(world, dream_uuid, realizer_uuid)
        ret_m = Message("award_winning", {"status":status_code})
        return ret_m
        
    # 取得 dream 資料
    def getDreamData(self, message):
        """
            收到的 message 格式
            title = "get_dream_data"
            contents = {"dream_uuid":"ddddddd-ddddd-dddd"}
            回傳的 message 格式
            title = "get_dream_data"
            contents = {"dream_name":"xxxxxxxx",
                        "dream_description":"xxxxxxx",
                        "dream_brief":"xxxxxxxxxxxx"
                        "dream_award":10
                        "dream_state":1,
                        "dream_dreamer_uuid":"ddddd-ddd-dd-dddd",
                        "dream_realizer_uuid_list":"rrrrr-rrr-rr-rr"}
        """
        case = LockedCase()
        dream_uuid = message.getContents()["dream_uuid"]
        ret_contents = case.getDreamData(dream_uuid)
        ret_m = Message("get_dream_data", ret_contents)
        return ret_m
        
    #取得登入玩家資料
    def getLoginedPlayer(self, message):
        """
            收到的 message 格式
            title = "get_logined_player"
            contents = {"player_uuid":"uuuu-uuuu-uuuu"}
            回傳的 message 格式
            title = "get_logined_player"
            contents = {"player_name":"xxxxxx", "player_prestige":10}
        """
        case = LockedCase()
        player_uuid = message.getContents()["player_uuid"]
        ret_contents = case.getLoginedPlayerData(player_uuid)
        ret_m = Message("get_logined_player", ret_contents)
        return ret_m