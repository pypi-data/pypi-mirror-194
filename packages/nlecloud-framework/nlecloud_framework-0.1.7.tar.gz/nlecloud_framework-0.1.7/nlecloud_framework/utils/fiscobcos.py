# _*_ coding:utf-8 _*_
"""
@File: fiscobcos.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 16:58
@LastEditors: cfp
@Description: fisco bcos的sdk实现
https://webasedoc.readthedocs.io/zh_CN/latest/docs/WeBASE-APP-SDK/api.html
"""
import hashlib
import json
import time
import requests


class FiscoHelper(object):
    def __init__(self, config: dict):
        self.fisco_config = config
        self.base_url = f"http://{config['ip']}:{config['port']}"

    def get_signature(self, is_test=False):
        """
        :param config: 配置信息
        :param is_test: 是否进入测试
        :return:
        """
        md5 = hashlib.md5()
        timestamp = str(int(time.time() * 1000))
        appKey = self.fisco_config.get("appKey")
        appSecret = self.fisco_config.get("appSecret")
        if is_test:
            timestamp = 1614928857832
            appKey = "fdsf78aW"
            appSecret = "oMdarsqFOsSKThhvXagTpNdoOcIJxUwQ"

        dataStr = str(timestamp) + appKey + appSecret
        md5.update(dataStr.encode("utf8"))
        signature = md5.hexdigest().upper()
        if is_test and signature == "EEFD7CD030E6B311AA85B053A90E8A31":
            print("算法正确")
        return timestamp, signature

    def register_app(self, *args, **kwargs):
        """
        :description: 注册应用
        :param args:
        :last_editors: cfp
        :return
        """
        timestamp, signature = self.get_signature()
        appKey = self.fisco_config["appKey"]
        url = f"{self.base_url}/WeBASE-Node-Manager/api/appRegister?appKey={appKey}&signature={signature}&timestamp={timestamp}"
        header = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        data = {
            "appIp": "127.0.0.1",
            "appPort": 10003,  #填写下你的应用端口
            "appLink": "http://127.0.0.1:10003"
        }
        response = requests.post(url,json=data)
        print(response.text)


    def chain_base_information(self,*args,**kwargs):
        """
        :description:查询链基本信息
        :param args:
        :last_editors: cfp
        :return
        """
        timestamp, signature = self.get_signature()
        appKey = self.fisco_config["appKey"]
        url = f"{self.base_url}/WeBASE-Node-Manager/api/basicInfo?appKey={appKey}&signature={signature}&timestamp={timestamp}"
        response = requests.get(url)
        data = response.json()
        print(data)
        return data


    def run(self):
        # timestamp,signature = self.get_signature()
        # print(timestamp,signature)
        self.chain_base_information()
        print(self.base_url)
        url2 = "http://192.168.68.71:5002/WeBASE-Front/1/web3/blockNumber"
        utl = "http://localhost:5002/WeBASE-Front/encrypt"
        signUserId = "3030235e503b41649cd4443010417d04"
        parms = {
            "returnPrivateKey":True
        }
        url3 = f"http://192.168.68.71:5004/WeBASE-Sign/user/{signUserId}/userInfo"
        url4 = f"http://192.168.68.71:5004/WeBASE-Sign/user/list/1/1/10"

        # 加密数据
        data = {
            "signUserId": "3030235e503b41649cd4443010417d04",
            "encodedDataStr": "0x7b2731273a2032337d"
        }
        url5 = f"http://192.168.68.71:5004/WeBASE-Sign/sign"
        response = requests.get(url=url5,json=data)

        print(response.text)





if __name__ == '__main__':
    config = {
        "ip": "192.168.68.71",
        "port": 5001,
        "appKey": "ZztLN9DF",
        "appSecret": "LtTf8GSQ2dVFn7m5jQTgLa8Fvxv9QbP3"
    }
    obj = FiscoHelper(config=config)
    obj.run()
