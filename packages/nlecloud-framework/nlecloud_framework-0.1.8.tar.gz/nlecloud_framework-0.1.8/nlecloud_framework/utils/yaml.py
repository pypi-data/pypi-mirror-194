# _*_ coding:utf-8 _*_
"""
@File: yaml.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 10:15
@LastEditors: cfp
@LastModifyTime @Version  @Desciption
@Description: yaml文件帮助类
"""
import yaml
import os
from pprint import pprint

class YamlHelper(object):

    def __init__(self):
        pass

    @classmethod
    def read_yaml(cls,path:str):
        """
        @description: 读取yaml文件并返回数据
        @param path: 文件路径
        @return
        @last_editors: cfp
        """
        # 读取YAML文件
        with open(path, 'r',encoding="utf8") as stream:
            try:
                yaml_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return yaml_data


    @classmethod
    def dump_yaml(cls,save_path:str,data:dict)->bool:
        """
        @description: 将数据转换为yaml格式
        @param save_path:到保存yaml的地址
        @param data:要转换YAML格式的数据
        @return
        @last_editors: cfp
        """
        # 将数据转换为YAML格式
        yaml_data = yaml.dump(data)
        # 将YAML数据写入文件
        if save_path:
            with open(save_path, 'w') as file:
                file.write(yaml_data)
        return True







