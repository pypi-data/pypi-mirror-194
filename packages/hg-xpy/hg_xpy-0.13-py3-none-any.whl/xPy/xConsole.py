# coding=utf-8
import signal
'''
Date: 2023-02-28
Description: 
LastEditTime: 2023-03-01
LastEditors: xushuwei
'''
import xLog


def signal_handler(signum, frame):

    if signum == signal.SIGINT.value:
        print("捕捉到Ctrl+C，退出程序")
        exit(-1)


def Init():
    xLog.Init()
    signal.signal(signal.SIGINT, signal_handler)
