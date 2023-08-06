# _*_ coding:utf-8 _*_
"""
@File: oss.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 10:13
@LastEditors: cfp
@LastModifyTime @Version  @Desciption
@Description: 对象存储帮助类
"""

import oss2
import os
from nlecloud_framework.utils.uuid import *


class OSSHelper(object):


    @classmethod
    def bucket_all(cls,oss_config:dict):
        """
        :param oss_config: 获取对应此oss有哪些oss
        :return:
        """
        ak_id = oss_config.get("ak_id", "")
        ak_secret = oss_config.get("ak_secret", "")
        service = oss2.Service(oss2.Auth(ak_id, ak_secret), 'https://oss-cn-hangzhou.aliyuncs.com')
        # 列举当前账号所有地域下的存储空间。
        bucket_names = []
        for b in oss2.BucketIterator(service):
            bucket_names.append(b.name)
        print("存在以下这些bucket：",bucket_names)
        return bucket_names


    @classmethod
    def oss_upload(cls,file_path:str,oss_config:dict,file_folder:str,bytes_data=bytes(),is_auto_name=True)->tuple:
        """
        :param file_path: 要上传的本地文件路径
        :param oss_config: oss的配置信息
        :param file_folder: 指定文件的前缀
        :param bytes_data: 字节数据
        :param is_auto_name: 是否自动名称
        :return:
        """
        if not file_folder:
            print("上传OSS必须文件所处文件夹名称！")
            return ""

        # 获取要上传的文件名称
        file_suffix = os.path.splitext(os.path.basename(file_path))[1] #获取文件后缀名称.py
        if is_auto_name:
            # 是否随机文件名
            file_name = UUIDHelper.get_uuid().replace("-", "") + file_suffix
        else:
            file_name = os.path.basename(file_path)

        file_name = file_folder.strip("/") +"/"+file_name
        print("oss文件名称：",file_name)

        # 获取oss的配置信息
        ak_id = oss_config.get("ak_id","")
        ak_secret = oss_config.get("ak_secret","")
        end_point = oss_config.get("end_point","")
        bucket_name = oss_config.get("bucket_name","")
        demain = oss_config.get("demain","")

        # oss认证
        auth = oss2.Auth(ak_id, ak_secret)
        bucket = oss2.Bucket(auth, end_point, bucket_name)

        # 上传文件
        # 如果需要上传文件时设置文件存储类型与访问权限，请在put_object中设置相关headers, 参考如下。
        # headers = dict()
        # headers["x-oss-storage-class"] = "Standard"
        # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
        # result = bucket.put_object('<yourObjectName>', 'content of object', headers=headers)
        if bytes_data:
            result = bucket.put_object(file_name, bytes_data)
        else:
            result = bucket.put_object_from_file(file_name, file_path)

        resource_path = ''
        if result.status == 200:
            resource_path = demain + file_name
            print(resource_path)
            # # HTTP返回码。
            # print('http status: {0}'.format(result.status))
            # # 请求ID。请求ID是请求的唯一标识，强烈建议在程序日志中添加此参数。
            # print('request_id: {0}'.format(result.request_id))
            # # ETag是put_object方法返回值特有的属性。
            # print('ETag: {0}'.format(result.etag))
            # # HTTP响应头部。
            # print('date: {0}'.format(result.headers['date']))
        return file_name,resource_path


    @classmethod
    def oss_remove(cls, file_name: str, oss_config: dict) -> bool:
        """
        :param file_name:删除oss的资源对象
        :param oss_config: oss的配置信息
        :param file_folder: 指定文件的前缀
        :param bytes_data: 字节数据
        :param is_auto_name: 是否自动名称
        :return:
        """
        # 获取oss的配置信息
        ak_id = oss_config.get("ak_id", "")
        ak_secret = oss_config.get("ak_secret", "")
        end_point = oss_config.get("end_point", "")
        bucket_name = oss_config.get("bucket_name", "")
        demain = oss_config.get("demain", "")

        # oss认证
        auth = oss2.Auth(ak_id, ak_secret)
        bucket = oss2.Bucket(auth, end_point, bucket_name)
        bucket.delete_object(file_name)

        if not cls.is_exist(file_name=file_name,oss_config=oss_config):
            return True
        else:
            return False


    @classmethod
    def is_exist(cls,file_name: str, oss_config: dict)->bool:
        """
        :param file_name:删除oss的资源对象
        :param oss_config: oss的配置信息
        :param file_folder: 指定文件的前缀
        :param bytes_data: 字节数据
        :param is_auto_name: 是否自动名称
        :return:
        """
        ak_id = oss_config.get("ak_id", "")
        ak_secret = oss_config.get("ak_secret", "")
        end_point = oss_config.get("end_point", "")
        bucket_name = oss_config.get("bucket_name", "")
        auth = oss2.Auth(ak_id, ak_secret)
        bucket = oss2.Bucket(auth, end_point, bucket_name)
        exist = bucket.object_exists(file_name)
        # 返回值为true表示文件存在，false表示文件不存在。
        return True if exist else False

