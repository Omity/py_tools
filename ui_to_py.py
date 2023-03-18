#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：ui_to_py.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/2/12 22:49

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""

# 库引入
import os
import os.path

# 变量声明
import time

root_directory = 'ui'
is_modify_time = 5 * 60
# 函数定义

# 类定义

# 更新过


def isModified(curr, file):
    create = os.path.getctime(file)
    modify = os.path.getmtime(file)
    if curr - create < is_modify_time:
        return True
    elif curr - modify < is_modify_time:
        return True

    return False


# 列出目录下的所有UI文件
def listUiFile(directory):
    # 避免需要转换的时间过长, 我们先把当前时间获取
    curr = time.time()
    a_list = []
    files = os.listdir(directory)
    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            a_list.extend(listUiFile(path))
        if os.path.isfile(path):
            # 对应的py文件不存在
            tmp = os.path.splitext(filename)[0] + '.py'
            if not os.path.exists(os.path.join(os.path.dirname(path), tmp)):
                a_list.append(path)
                continue
            if isModified(curr, path):
                if os.path.splitext(filename)[1] == '.ui':
                    a_list.append(path)
    return a_list


# 把扩展名为.ui的文件改成扩展名为.py的文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# 调用系统命令把UI文件转换成Python文件
def runMain(directory):
    a_list = listUiFile(directory)
    for uiFile in a_list:
        pyFile = transPyFile(uiFile)
        cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyFile, uifile=uiFile)
        os.system(cmd)


if __name__ == "__main__":
    current = os.getcwd()
    runMain(os.path.join(current, root_directory))
