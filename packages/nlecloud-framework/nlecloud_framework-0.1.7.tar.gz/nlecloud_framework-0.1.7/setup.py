# _*_ coding:utf-8 _*_
"""
@File: setup.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/22 15:43
@LastEditors: cfp
@LastModifyTime @Version  @Desciption
@Description: 
"""

from distutils.core import setup
from setuptools import find_packages

# 获取readme文档
with open("README.md", "rb") as f:
    data = f.read().decode("utf8")
    long_description = data

# 需要安装的第三方库列表
# utf16leToUtf8("requirement.txt","requirement.txt")
# with open("requirement.txt", "r", encoding="utf8") as f:
#     install_requires_list = stringTextLine_to_list(f.read(), is_print=True)

install_requires_list = ['aliyun-python-sdk-core==2.13.36',
                         'aliyun-python-sdk-kms==2.16.0',
                         'certifi==2022.12.7',
                         'cffi==1.15.1',
                         'chardet==5.1.0',
                         'charset-normalizer==3.0.1',
                         'crcmod==1.7',
                         'cryptography==39.0.1',
                         'idna==3.4',
                         'jmespath==0.10.0',
                         'oss2==2.16.0',
                         'pycparser==2.21',
                         'pycryptodome==3.17',
                         'PyYAML==6.0',
                         'requests==2.28.2',
                         'six==1.16.0',
                         'urllib3==1.26.14',
                         'attrdict',
                         'bumpversion<1,>=0.5.3',
                         'configobj',
                         'cytoolz',
                         'lru-dict',
                         'parsimonious',
                         'pycryptodome',
                         'cryptography>=3.3.1',
                         'requests',
                         'toolz',
                         'hypothesis>=3.6.1',
                         'argcomplete',
                         'pymitter',
                         'asyncio',
                         'promise',
                         'rsa',
                         'ecdsa',
                         'pyOpenSSL==20.0.0']


setup(
    name="nlecloud_framework",  # python包的名字
    version="0.1.7",  # 版本号
    description='nlecloud_framework框架',  # 描述
    long_description=long_description,  # 详细描述，这里将readme的内容放置于此
    long_description_content_type='text/markdown',  # 文件格式
    author='cfp',  # 作者
    author_email='954742660@qq.com',  # 作者邮箱
    maintainer='dalyer',  # 维护人
    maintainer_email='954742660@qq.com',  # 维护人邮箱
    license='BSD License',  # 遵守协议
    packages=find_packages(),
    install_requires=install_requires_list,  # lamb-common依赖的第三方库,
    platforms=["all"],  # 支持的平台
    url='https://gitee.com/daliyup0518/nlecloud_framework.git',  # github代码仓地址
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries'
    ],
)
