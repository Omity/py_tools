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
import time
import zipfile
import shutil

import common.project_info as pi

# 变量声明
valid_time = 1 * 60
abspath = os.path.dirname(os.path.abspath(__file__))
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


def updateHelper(path, target):
    if checkUpdateValid(path):
        file = zipfile.ZipFile(path)
        file.extractall(target)
        file.close()
        shutil.rmtree(os.path.dirname(path))
        # os.remove(os.path.dirname(path))


# 类定义


if __name__ == '__main__':
    f = os.path.join(abspath, f"{pi.PROJECT_UPDATE_DIR}/{pi.PROJECT_UPDATE_FILE}")
    updateHelper(f, abspath)
