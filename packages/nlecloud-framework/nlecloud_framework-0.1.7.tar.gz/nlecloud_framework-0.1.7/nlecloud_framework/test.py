# _*_ coding:utf-8 _*_
"""
@File: test.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 10:42
@LastEditors: cfp
@Description: 测试模块
"""
import oss2

from utils.uuid import UUIDHelper
from utils.yaml import YamlHelper
from utils.crypto import CryptoHelper
from utils.oss import OSSHelper
from pprint import pprint
import sys
from nlelib.fiscobcos_sdk.client_config import client_config
import os
import json
import os


if __name__ == '__main__':
    print(json.dumps(sys.path))
    print(client_config.bcos3_config_file)
    # project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # config_path = os.path.join(project_path, "config.yaml")
    # config_data = YamlHelper.read_yaml(config_path)
    #
    # # 加密库
    # key = CryptoHelper.genRandomKey()
    # config_data["crypto_key"] = key
    # YamlHelper.dump_yaml(config_path, config_data)
    # p = CryptoHelper.plain_to_ciphert(key, "我的密码是123456")
    # print("加密后的数据", p)
    # c = CryptoHelper.cipher_to_plain(key, p)
    # print("解密后的数据", c)
    #
    # # uuid
    # # print(UUIDHelper.get_uuid())
    #
    # # oss
    # path = r"C:\Users\Administrator\Desktop\11.xlsx"
    # file_name,resource_path = OSSHelper.oss_upload(path,config_data["oss_config"],"test")
    # print(OSSHelper.is_exist(file_name,config_data["oss_config"]))
    # print(OSSHelper.oss_remove(file_name,config_data["oss_config"]))

