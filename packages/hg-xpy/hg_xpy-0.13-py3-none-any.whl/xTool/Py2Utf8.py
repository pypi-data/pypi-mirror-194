# -*- coding: utf-8 -*-
'''
Date: 2023-02-28
Description: 给py文件第一行加入UTF8编码
LastEditTime: 2023-02-28
LastEditors: xushuwei
'''


import os
import logging
import codecs
from xPy import Encode


def head_set_utf8(dir_path):
    for curr, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".py"):
                continue
            fpath = os.path.join(curr, file)
            Encode.Convert2Utf8(fpath)


# 默认寻找当前目录下的python文件
def Run(dir_path=None):
    dir_path = dir_path if dir_path else os.getcwd()
    if not os.path.exists(dir_path):
        logging.warn(f'path not exist:{dir_path}')
        return
    head_set_utf8(dir_path)


def Convert2Utf8(filename: str):
    content, old_encoding = Encode.GetFileContent(filename)
    if old_encoding == 'utf-8':
        return

    first_line = content.split("\n")[0]
    if first_line.find('utf') != -1 and first_line.find('8') != -1:
        return

    f = codecs.open(filename, 'w', encoding='utf-8')
    f.seek(0, 0)
    f.write("# coding=utf-8\n\r" + content)

    logging.info(f'{old_encoding} ==> utf-8 success:{filename}')
