# coding=utf-8
'''
Date: 2022-09-27
LastEditTime: 2023-03-01
Description: python多线程
'''

import multiprocessing
import subprocess
import queue
import logging
import sys
import threading


def GetStr(str):
    try:
        str = str.decode("utf8")
    except:
        str = str.decode("gbk")
    finally:
        pass
    return str


def _ThreadProcess(id: int, queue, lock, failed_cmd):
    logging.info("thread[%d]    start......." % id)
    while True:
        cmd = queue.get()
        with lock:
            sys.stdout.write("\n[%d]    staring.....\n%s\n" %
                             (id, ' '.join(cmd)))

        proc = subprocess.Popen(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, err = proc.communicate()
        output = GetStr(output)
        err = GetStr(err)

        if proc.returncode != 0:
            failed_cmd.append(cmd)
        with lock:
            sys.stdout.write("\n[%d]    done:%s" % (id, output))
            if len(err) > 0:
                sys.stdout.flush()
                sys.stderr.write("\n[%d]    error:%s" % (id, err))
        queue.task_done()


def Start(cmds, max_task=3):
    task_queue = queue.Queue(max_task)
    # List of files with a non-zero return code.
    failed_cmd = []
    lock = threading.Lock()
    for i in range(max_task):
        t = threading.Thread(
            target=_ThreadProcess, args=(i, task_queue, lock, failed_cmd)
        )
        t.daemon = True
        t.start()

    for c in cmds:
        task_queue.put(c)

    # Wait for all threads to be done.
    task_queue.join()
    str = ''
    for c in failed_cmd:
        str = str + '\r\n' + ' '.join(c)
    logging.info(str)
    return len(failed_cmd) == 0
