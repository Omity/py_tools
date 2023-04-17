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
import zipfile
import common.project_info as pi
import shutil
import tools.py_tools_helper as ph

# 变量声明
mainFile = 'main.py'
packName = 'py_tools'
helperFile = 'tools/py_tools_helper.py'
helperSrc = ['update/project_ino.py']
helperPack = 'helper'
log_level = 'WARN'
abspath = os.path.dirname(os.path.abspath(__file__))
# 函数定义
# def 
# 类定义


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
            # 存储在打包后的同名文件夹下
            a_list.append(path + f';{os.path.basename(directory)}')
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

######################################
# 升级包目前是打包所有的压缩文件进行升级, 后期
# 将考虑是否以增量形式进行远程升级
######################################


def zipFile(_dir, out):
    """
    升级包不需要tools里面的exe文件, 需要在形成打包安装文件之前调用
    :param _dir:
    :param out:
    :return:
    """
    if not os.path.exists(os.path.dirname(out)):
        os.mkdir(os.path.dirname(out))
    f = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    for path, dirname, file in os.walk(_dir):
        fpath = path.replace(_dir, '')
        for filename in file:
            f.write(os.path.join(path, filename), os.path.join(fpath, filename))
    f.close()


def packMain():
    ico = f" -i {scanIco(os.path.join(abspath, 'data'))[0]}"
    cmd = f"pyinstaller -y {mainFile} --noconsole --clean --log-level {log_level}"
    for i in scanSrc(os.path.join(abspath, 'api')):
        cmd += f" -p {i}"
    for i in scanSrc(os.path.join(abspath, 'ui')):
        cmd += f" -p {i}"
    for i in scanSrc(os.path.join(abspath, 'common')):
        cmd += f" -p {i}"
    for i in scanData(os.path.join(abspath, 'data')):
        cmd += f" --add-data {i}"

    # cmd += f" --add-data {os.path.join(abspath, 'helper.exe')};{os.path.join(abspath, 'tools')}"

    # 打包后的目录名字, 注意yml文件对应打包的时候需要对应
    cmd += f"{ico} -n {packName}"

    # force to include the dependency
    cmd += f" --collect-all charset_normalizer"

    os.system(cmd)


def packHelper():
    """

    :return:
    """
    ico = f" -i {scanIco(os.path.join(abspath, 'data'))[0]}"
    cmd = f"pyinstaller -y -F {helperFile} --noconsole --clean --log-level {log_level}"
    for i in helperSrc:
        cmd += f" -p {i}"
    cmd += f"{ico} -n {helperPack}"
    os.system(cmd)


def copyHelper(_from, _to):
    files = os.listdir(_from)
    for file in files:
        if os.path.splitext(file)[1] == '.exe':
            if not os.path.exists(_to):
                os.mkdir(_to)
            shutil.copy(os.path.join(_from, file), os.path.join(_to, file))


if __name__ == '__main__':

    # ico = ' -i ' + scanIco('data')[0]
    # cmd = pyinstaller + ' -y ' + mainFile
    # for i in scanSrc('api'):
    #     cmd += ' -p ' + i
    # for i in scanSrc('ui'):
    #     cmd += ' -p ' + i
    #
    # for i in scanData('data'):
    #     cmd += data + i
    #
    # cmd += ico
    # cmd += noConsole
    # # 打包后的目录名字, 注意yml文件对应打包的时候需要对应
    # cmd += '-n ' + packName

    # os.system(cmd)
    packHelper()
    packMain()
    zipFile(os.path.join('dist', packName), os.path.join(abspath, pi.PROJECT_UPDATE_FILE))
    copyHelper(f'./dist', f'./dist/{packName}/tools')
    # zipFile(os.path.join('dist', packName), f"update/{pi.PROJECT_UPDATE_FILE}")
    # ph.updateHelper(os.path.join(f'tmp', pi.PROJECT_UPDATE_FILE), 'tmp')
