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
import time

import project_info as pro
import version as ver
import requests
import zipfile
from bs4 import BeautifulSoup

# 变量声明
GITHUB_PATH = r'https://github.com'
GITEE_PATH = r'https://ghproxy.com/https://gitee.com'
UPDATE_PATH = f'{GITHUB_PATH}/{pro.PROJECT_AUTHOR}/{pro.PROJECT_NAME}/releases/latest'


# 函数定义
# def 
# 类定义


class ProjectUpdate:

    def __init__(self, server, current_version: list, update_pack, headers=None, callback=None):
        self.server = server  # 服务器地址
        self.current_version = current_version  # 当前版本  如[0, 1, 1] v0.1.1
        self.callback = callback
        self.update_pack = update_pack  # 升级包名字
        self.headers = headers
        self.request = requests.session()

    def getUpdateInfo(self, owner, project):
        """
        获取版本信息
        :param owner:  服务器拥有者
        :param project: 工程名
        :return:
        """
        url = f'{self.server}/{owner}/{project}/releases/latest'
        print('url is ', url)
        json = self.request.get(url)
        return self.decodeUpdate(json.text, owner, project)

    def decodeUpdate(self, txt, owner, project):
        """
        解析网页, 获取版本信息
        :param project:
        :param owner:
        :param txt:
        :return:
        """
        print('decode')
        bs = BeautifulSoup(txt, "html.parser")
        version = bs.find('h1', class_='d-inline mr-3').text
        comment = bs.find('div', class_='markdown-body my-3').text
        return {
            'version': version,
            'comment': comment,
            'download': f'{self.server}/{owner}/{project}/download/{version}/{self.update_pack}'
        }

    def downloadUpdate(self, file, local):
        """
        下载
        :param file:
        :param local:
        :return:
        """
        print('get zip', file)
        # noinspection PyBroadException
        try:
            out = requests.get(file, stream=True)
            print(int(out.headers.get('content-length')))
            with open(f'{local}/{self.update_pack}', 'wb') as f:
                for chunk in out.iter_content(chunk_size=10 * 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                return True
        except Exception:
            print('failed')
            return False

    @staticmethod
    def unzip(_from, _to):
        """
        解压缩文件
        :param _from:
        :param _to:
        :return:
        """
        file = zipfile.ZipFile(_from)
        file.extractall(_to)
        file.close()
        os.remove(_from)

    def update(self, owner, project, download, install):
        """
        升级
        :param owner: 服务器账号名
        :param project: 工程名
        :param download: 本地下载路径
        :param install: 软件安装路径
        :return:
        """
        # 获取版本新信息
        info = self.getUpdateInfo(owner, project)
        version = list(map(int, info['version'].replace('v', '').split('.')))

        # 需要版本更新
        if version[0] > self.current_version[0] or version[1] > self.current_version[1] \
                or version[2] > self.current_version[2]:
            print('update')
            if self.downloadUpdate(info['download'], download):
                # self.unzip(download, install)
                print('end')
                return True
            else:
                return False
        return False


def 下载文件(url, 保存地址, 回调函数=None):
    # 回调函数例子
    #     def 进度(进度百分比, 已下载大小, 文件大小, 下载速率, 剩余时间):
    #         信息 = f"进度 {进度百分比}% 已下载 {已下载大小}MB 文件大小 {文件大小}MB 下载速率 {下载速率}MB 剩余时间 {剩余时间}秒"
    #         print(f"\r {信息}", end="")
    if 回调函数:
        start_time = time.time()
    r = requests.get(url, stream=True)
    # print('pass')
    with open(保存地址, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        print(total_length)
        # 获取百分比 并调用回调函数
        for chunk in r.iter_content(chunk_size=10 * 1024):
            if chunk:
                f.write(chunk)
                f.flush()
                if 回调函数:
                    # 转化为百分比
                    进度百分比 = int(f.tell() * 100 / total_length)
                    已下载大小 = f.tell() / 1024 / 1024
                    文件大小MB = total_length / 1024 / 1024
                    下载速率MB = 已下载大小 / (time.time() - start_time)
                    # 获取剩余时间取秒
                    剩余时间 = (文件大小MB - 已下载大小) / 下载速率MB
                    剩余时间 = int(剩余时间)
                    # 所有数据保留两位小数
                    下载速率MB = round(下载速率MB, 2)
                    文件大小MB = round(文件大小MB, 2)
                    已下载大小 = round(已下载大小, 2)
                    进度百分比 = round(进度百分比, 2)
                    回调函数(进度百分比, 已下载大小, 文件大小MB, 下载速率MB, 剩余时间)
    return True

class Update:

    def __init__(self, target='https://github.com/Omity/py_tools/releases', features='html.parser',
                 proxy='https://ghproxy.com', github='https://github.com'):
        self.target = target
        self.features = features
        self.proxy = proxy
        self.github = github
        self.request = requests.Session()

    def getHtml(self, des):
        """
        获取指定网页内容
        :param des:
        :return:
        """
        try:
            return self.request.get(f'{self.target}/{des}').text
        except requests.exceptions.ConnectionError:
            return self.request.get(f'{self.proxy}/{self.target}/{des}').text

    def getLatestVer(self):
        """
        获取最新版本
        :return:
        """
        bf = BeautifulSoup(self.getHtml('latest'), self.features)
        # 最新版本号位于<span class='ml-1'里面, 且应该是只有一个
        return bf.select('span .ml-1')[0].get_text().strip()

    def getUpdateInfo(self):
        """
        获取更新内容和下载地址
        :return: 更新内容和下载文件地址, 格式: {'update_info': str, 'url': []}
        """
        _data = {
            'update_info': '',
            'url': []
        }
        bf = BeautifulSoup(self.getHtml('latest'), self.features)
        # 更新内容位于<div ... class='markdown-body my-3'的子标签ul里面
        _data['update_info'] = bf.select('div .markdown-body > ul')[0].get_text().strip()
        # 下载地址需要重新获取网页
        bf = BeautifulSoup(self.getHtml(f'expanded_assets/{self.getLatestVer()}'), self.features)
        tmp = bf.select('div .d-flex > a')
        for i in tmp:
            _data['url'].append(f'{self.proxy}/{self.github}{i["href"]}')

        return _data

    def downUpdateZip(self, url, save):
        """
        下载指定路径的文件
        :param save:
        :param url:
        :return:
        """
        rps = self.request.get(url, stream=True)
        name = url.split('/')[-1]
        print('start')
        with open(os.path.join(save, name), 'wb') as f:
            for chunk in rps.iter_content(chunk_size=10 * 1024):
                if chunk:
                    f.write(chunk)
                    f.flush()


if __name__ == '__main__':
    he = {"user-agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) "
                        "Chrome / 75.0.3770.100Safari / 537.36"}
    # a = ProjectUpdate(GITHUB_PATH, [0, 0, 1], 'my_app.exe')
    # a.downloadUpdate('https://github.com/duolabmeng6/qtAutoUpdateApp/download/v0.0.62/my_app.exe', 'dist')
    下载文件('https://github.com/duolabmeng6/qtAutoUpdateApp/download/v0.0.62/my_app.exe', 'dist/my_app.exe')
