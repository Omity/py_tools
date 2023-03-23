#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: git_test.py
功能描述: 测试功能是否可用, 推送到develop分支进行测试
作者: ShuJie
版本: V0.1
创建时间: 2023/3/18 18:59

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入
import os


# 变量声明
DEVELOP_PATH = 'develop'
COMMIT_INFO = 'release v0.0.5'
# 函数定义
# def 
# 类定义


if __name__ == '__main__':
    print('Info: Note that this action commits all the modified and new files\n')
    print(f'Info: Prepare to push code to remote branch {DEVELOP_PATH}\n')
    print('Info: You can view the results of the workflow in GitHub\'s actions\n')
    os.system('git add .')
    os.system(f'git commit -m "{COMMIT_INFO}"')
    os.system(f'git push origin {DEVELOP_PATH}')
