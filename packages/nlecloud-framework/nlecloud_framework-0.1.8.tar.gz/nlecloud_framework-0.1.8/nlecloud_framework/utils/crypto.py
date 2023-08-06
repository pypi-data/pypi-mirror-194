# _*_ coding:utf-8 _*_
"""
@File: crypto.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/22 17:52
@LastEditors: cfp
@Description: 框架加密库
"""

from cryptography.fernet import Fernet
import base64

class CryptoHelper(object):

    @classmethod
    def genRandomKey(cls)->str:
        """
        @description: 生成一个随机的秘钥
        @param :
        @return 返回字符串经过base64的key
        @last_editors: cfp
        """
        key = Fernet.generate_key()
        key_b64 = base64.urlsafe_b64encode(key).decode('utf-8')
        return key_b64


    @classmethod
    def plain_to_ciphert(cls,key:str,plaintext:str)->str:
        """
        @description: 对数据进行加密
        @param key: 秘钥
        @param plaintext:要加密的数据
        @return
        @last_editors: cfp
        """
        # 将key转成字节
        key = base64.urlsafe_b64decode(key)

        # 对数据进行加密
        cipher_suite = Fernet(key)
        plaintext = plaintext.encode("utf8")
        ciphertext = cipher_suite.encrypt(plaintext)
        # 密文转换成base64编码字符串
        ciphertext_b64 = base64.urlsafe_b64encode(ciphertext).decode('utf-8')
        return ciphertext_b64


    @classmethod
    def cipher_to_plain(cls,key:str,ciphertext:str)->str:
        """
        @description:
        @param key: 秘钥
        @param ciphertext:加密的数据
        @return
        @last_editors: cfp
        """
        # 将base64密文解码
        key = base64.urlsafe_b64decode(key)
        ciphertext = base64.urlsafe_b64decode(ciphertext)
        # 创建一个Fernet对象，并使用密钥解密密文
        cipher_suite = Fernet(key)
        plaintext = cipher_suite.decrypt(ciphertext)

        # 打印解密后的数据
        return plaintext.decode("utf8")



