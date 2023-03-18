#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: git_push.py
功能描述: push代码到release分支进行发布
作者: ShuJie
版本: V0.1
创建时间: 2023/3/18 17:59

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入

# 变量声明
import os

RELEASE_PATH = 'test'
COMMIT_INFO = 'test for info'
# 函数定义
# def 
# 类定义


if __name__ == '__main__':
    print('Info: Note that this action commits all the modified and new files\n')
    print(f'Info: Prepare to push code to remote branch {RELEASE_PATH}\n')
    os.system('git add .')
    os.system(f'git commit -m "{COMMIT_INFO}"')
    os.system(f'git push origin {RELEASE_PATH}')
