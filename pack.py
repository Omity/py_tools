#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：pack.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/10/4 19:17

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""
# 库引入
import os

# 变量声明
# G_para = '' 
# 函数定义
# def 
# 类定义
import sys

pyinstaller = r'venv\Scripts\pyinstaller.exe '
mainFile = 'main.py'
sourceFile = ['ascii.py', 'asciiTool.py', 'conversion.py', 'conversionTool.py', 'serial_tool.py', 'serialTool.py',
              'pytools.py']
resource = ['ascii_info.html;.']
icoPic = 'py_tool.ico'
noConsole = ' --noconsole '
outPath = ' --distpath '
tempPath = ' --workpath '
specPath = ' -o '
data = ' --add-data '
packName = 'py_tools'


def scanSrc(directory):
    a_list = []
    files = os.listdir(directory)
    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            a_list.extend(scanSrc(path))
        if os.path.isfile(path):
            if os.path.splitext(filename)[1] == '.py':
                a_list.append(path)
    return a_list


def scanData(directory):
    a_list = []
    files = os.listdir(directory)
    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            a_list.extend(scanSrc(path))
        if os.path.isfile(path):
            a_list.append(path + f';{directory}')
    return a_list


def scanIco(directory):
    a_list = []
    files = os.listdir(directory)
    for filename in files:
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            a_list.extend(scanSrc(path))
        if os.path.isfile(path):
            # 排除ico
            if os.path.splitext(filename)[1] == '.ico':
                a_list.append(path)
    return a_list


if __name__ == '__main__':

    current = os.getcwd()
    print(current)

    pyinstaller = os.path.join(current, pyinstaller)

    ico = ' -i ' + scanIco('data')[0]
    cmd = pyinstaller + ' -y ' + mainFile
    for i in scanSrc('api'):
        cmd += ' -p ' + i
    for i in scanSrc('ui'):
        cmd += ' -p ' + i

    for i in scanData('data'):
        cmd += data + i

    cmd += ico
    cmd += noConsole
    # 打包后的目录名字, 注意yml文件对应打包的时候需要对应
    cmd += '-n ' + packName

    os.system(cmd)
