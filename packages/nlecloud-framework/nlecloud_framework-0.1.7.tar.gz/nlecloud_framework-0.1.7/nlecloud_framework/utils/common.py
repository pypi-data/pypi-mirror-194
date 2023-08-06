# _*_ coding:utf-8 _*_
"""
@File: common.py
@Author: cfp
@Date: 2020-08-21 14:07:08
@LastEditTime: 2023/2/23 14:21
@LastEditors: cfp
@Description: 常用转换工具
"""
import os
from pprint import pprint
import chardet


def stringTextLine_to_list(str_lines,is_print=True)->list:
    """
    :description: 按每行文本转换成列表
    :param str_lines:要转换的字符串文本行
    :last_editors: cfp
    :return
    """
    data = str_lines.split("\n")
    temp = []
    for i in data:
        i = i.strip()
        if i:
            temp.append(i)
    if is_print:
        print("输出转换好的文本信息")
        pprint(temp)
    return temp



def utf16leToUtf8(infile, outfile):
    """
    :description: utf-16 le 格式转为utf-8
    :param infile: 输入文件
    :param outfile: 输出文件
    :return:
    """
    # 文件是utf-16 le编码，故只读取这种，也有不是这种编码的，如果不成功就有可能抛出异常，因此为了避免程序停止，需要捕获异常
    try:
        # 判断文件编码是否是UTF-16
        with open(infile,"rb") as f :
            content = f.read()
            result = chardet.detect(content)
            if "utf-16" not in result["encoding"].lower():
                return None

        # 文件重新保存
        with open(outfile, "w", encoding='utf-8') as f1:
            content = stringTextLine_to_list(content.decode("utf-16"))
            print(content)
            content = "\n".join(content)
            f1.write(content)

    except UnicodeDecodeError:
        print("UnicodeDecodeError err%s" % infile)


if __name__ == '__main__':
    print()





