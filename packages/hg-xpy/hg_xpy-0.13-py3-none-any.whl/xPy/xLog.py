# coding=utf-8
'''
Date: 2023-02-28
Description: 
LastEditTime: 2023-03-01
LastEditors: xushuwei
'''
import logging
import os
from datetime import datetime
from rich.logging import RichHandler


def Init():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(log_time_format="[%X]")],
    )
    if not os.path.exists("log"):
        os.mkdir("log")
    logger = logging.getLogger()
    logger.setLevel("INFO")

    BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    fhlr = logging.FileHandler(
        "log/py_{:%Y-%m-%d}.log".format(datetime.now())
    )  # 输出到文件的handler
    fhlr.setLevel("INFO")  # 也可以不设置，不设置就默认用logger的level
    fhlr.setFormatter(formatter)
    logger.addHandler(fhlr)
