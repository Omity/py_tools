#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：update.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/10/16 15:23

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""
# 库引入
import os

import requests
from bs4 import BeautifulSoup


# 变量声明

# 函数定义
# def 
# 类定义


class ProjectUpdate(object):

    def __init__(self, server, headers=None, callback=None, features='html.parser', proxy='https://ghproxy.com',
                 timeout=10, *args, **kwargs):
        self.server = server  # 服务器地址
        self.callback = callback
        self.features = features
        self.proxy = proxy
        self.headers = headers if headers is not None else {"user-agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) "
                                                                          "AppleWebKit / 537.36(KHTML, likeGecko) "
                                                                          "Chrome / 75.0.3770.100Safari / 537.36"}
        self.request = requests.Session()
        self.size = 0
        self.chunk = 50 * 1024
        self.breaks = False
        self.failInfo = 'get server information failed'
        self.timeout = timeout
        self.latest = []

    def setCallback(self, call):
        self.callback = call

    def setChunk(self, chunk):
        self.chunk = chunk

    def getHtml(self, des):
        """
        获取网页地址
        :param des:
        :return:
        """
        # noinspection PyBroadException
        try:
            return self.request.get(f'{self.server}/{des}', timeout=self.timeout).text
        # except requests.exceptions.ConnectionError or requests.exceptions.SSLError or requests.exceptions.ReadTimeout:
        except Exception:
            print('try to get server: ', f'{self.proxy}/{self.server}/{des}')
            # noinspection PyBroadException
            try:
                return self.request.get(f'{self.proxy}/{self.server}/{des}', timeout=self.timeout).text
            # except requests.exceptions.ConnectionError or requests.exceptions.SSLError or \
            #         requests.exceptions.ReadTimeout:
            except Exception:
                return ''
        # finally:
        #     print('finally')
        #     return ''

    def getLatestVersion(self):
        """
        检查最新版本号
        :return:
        """
        bs = BeautifulSoup(self.getHtml('releases/latest'), self.features)
        # 最新版本号位于<span class='ml-1'里面, 且应该是只有一个
        # noinspection PyBroadException
        try:
            return bs.select('span .ml-1')[0].get_text().strip()
        except Exception:
            return None

    def isVersionBehind(self, version: list):
        """
        查询版本是否落后
        :param version:
        :return:
        """
        # 版本格式[x, x, x]
        if not version:
            return False
        print('check version')
        self.latest = self.getLatestVersion()
        if not self.latest:
            return False
        print('get version: ', self.latest)
        latest_ver = list(map(int, self.latest.replace('v', '').split('.')))
        if latest_ver[0] > version[0] or latest_ver[1] > version[1] or \
                latest_ver[2] > version[2]:
            return True
        return False

    def getUpdateInfo(self):
        """
        获取版本信息
        :return:
        """
        bs = BeautifulSoup(self.getHtml('releases/latest'), self.features)
        # 更新内容位于<div ... class='markdown-body my-3'的子标签ul里面
        # noinspection PyBroadException
        try:
            return bs.select('div .markdown-body > ul')[0].get_text().strip()
        except Exception:
            return self.failInfo

    def downloadPack(self, online_pack, local):
        """
        下载升级包
        :param online_pack:
        :param local:
        :return:
        """
        if not os.path.exists(local):
            os.mkdir(local)
        if not self.latest:
            self.latest = self.getLatestVersion()
        url = f'{self.proxy}/{self.server}/releases/download/{self.latest}/{online_pack}'
        tryUrl = f"{self.server}/releases/download/{self.getLatestVersion()}/{online_pack}"
        # noinspection PyBroadException
        try:
            print('try to get upgrade server: ', url)
            data = self.request.get(url, stream=True, timeout=self.timeout)
        except Exception or requests.exceptions.ReadTimeout:
            print('try to get upgrade server: ', url)
            data = self.request.get(tryUrl, stream=True, timeout=self.timeout)
        # noinspection PyBroadException
        try:
            # data = self.request.get(url, stream=True)
            self.size = int(data.headers['Content-Length'])
            print(f'upgrade zip file size: {self.size / 1024 / 1024}MB')
            with open(os.path.join(local, online_pack), 'wb') as f:
                for chunk in data.iter_content(chunk_size=self.chunk):
                    if self.breaks:
                        return False
                    # print('chunk xxx ')
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        print('write end')
                        if self.callback:
                            self.callback(self.chunk)
            return True
        except Exception or requests.exceptions.ReadTimeout as e:
            print(e)
            print('download upgrade zip failed')
            return False


if __name__ == '__main__':
    he = {"user-agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) "
                        "Chrome / 75.0.3770.100Safari / 537.36"}

    obj = ProjectUpdate('https://github.com/Omity/py_tools')
    print(obj.isVersionBehind([0, 0, 4]))
    print(obj.latest)
    print(obj.getUpdateInfo().split('\n'))
