#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: version_update.py
功能描述: 更新仓库里所有涉及到版本号的文件, 形成统一
作者: ShuJie
版本: V0.1
创建时间: 2023/3/18 16:54

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入
import re
from common import version

# 变量声明


file_to_change = ['inno_set_for_workflow.iss', 'py_tools.iss']
# 函数定义


def find_info_to_change(file, fuzzy):
    """
    寻找指定修改的内容
    :param fuzzy:
    :param file:
    :return:
    """

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if re.search(fuzzy, line):
                return re.search(fuzzy, line).group()


def change_info(file, line, _old, _new):
    """
    修改文件指定内容
    :param file: 文件路径
    :param line: 指定的内容
    :param _old: 指定修改的内容
    :param _new: 替换的内容
    :return:
    """
    data = ''
    with open(file, 'r', encoding='utf-8') as f:
        for li in f:
            if line in li:
                li = li.replace(_old, _new)
            data += li
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data)


def update_iss():
    new = f'{version.VERSION_MAIN}.{version.VERSION_SUB}.{version.VERSION_FIX}'
    for files in file_to_change:
        old = find_info_to_change(files, r'[0-9]+.[0-9]+.[0-9]+')
        change_info(files, "#define MyAppVersion", old, new)

# 类定义


if __name__ == '__main__':
    update_iss()
