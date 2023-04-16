#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: py_tools_helper.py
功能描述: 
作者: ShuJie
版本: V0.1
创建时间: 2023/3/31 19:54

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入
import os
import sys
# import time
import time
import zipfile

# import shutil

# import common.project_info as pi

# 变量声明
valid_time = 1 * 60


# abspath = os.path.dirname(os.path.abspath(__file__))
# 函数定义


def checkUpdateValid(path):
    """
    检测是否升级有效
    :param path:
    :return:
    """
    if os.path.exists(path):
        # if time.time() - os.path.getmtime(path) < valid_time:
        return True
    return False


def updateHelper(path, dst):
    if checkUpdateValid(path):
        print(path, dst)
        with zipfile.ZipFile(path, 'r') as zf:
            zf.extractall(dst)
            # for path in zf.namelist():
            #     print(path)
            #     zf.extract(path, dst)
        # os.remove(os.path.dirname(path))


# 类定义
class Logger(object):

    def __init__(self, log, stream=sys.stdout):
        self.f = open(log, 'a', encoding='utf-8')
        self.stream = stream

    def write(self, string):
        self.stream.write(string)
        self.f.write(string)
        self.f.flush()

    def flush(self):
        self.stream.flush()


if __name__ == '__main__':
    sys.stdout = Logger('logger.txt', sys.stdout)
    sys.stderr = Logger('logger.txt', sys.stderr)
    time.sleep(1)
    print(sys.argv, 'len is ', len(sys.argv))
    if len(sys.argv) > 2:
        print('sys argv: ', sys.argv[0], sys.argv[1])
        file = sys.argv[0]
        exe = sys.argv[1]
        target = sys.argv[2]
        if 'zip' in file and 'exe' in exe:
            print('can update')
            updateHelper(file, target)
            os.execv(exe, [exe])
    else:
        updateHelper(f'../update.zip',
                     r'../')
        os.system(r'../py_tools.exe')
    # f = os.path.join(abspath, f"{pi.PROJECT_UPDATE_FILE}")
    # updateHelper(f, abspath)
    # print(os.path.dirname(abspath))
