#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: lifeTool.py
功能描述: 
作者: ShuJie
版本: V0.1
创建时间: 2023/4/12 20:08

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入
import json
import os
import re
import sys
import time
import requests
import socket
from PyQt5.QtCore import QThread, QTimer

from PyQt5.QtWidgets import QWidget, QApplication
from bs4 import BeautifulSoup

from ui.life import Ui_life


# 变量声明
# G_para = '' 
# 函数定义
# def 
# 类定义


class Worker(QThread):

    def __init__(self, call, delay=2):
        super().__init__()
        self.call = call
        self.delay = delay

    def run(self):
        while True:
            self.call()
            QThread.sleep(self.delay)


class LifeTool(QWidget, Ui_life):
    _share_url = 'https://wttr.in/'

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setupUi(self)
        self.startTimer(1000)
        self.request = kwargs.get('session') if kwargs.get('session') is not None else requests.Session()
        self.timer = QTimer(self)
        self.work = Worker(self.getInfo)
        self.work.start()

    def getInfo(self):
        try:
            r = self.request.get(self._share_url)
            txt = r.text.split('\n')
            # print(txt)
            if len(txt) < 12:
                return
            # print(txt)
            self.addrInfo.setText(f"{txt[0].split(':')[-1].strip()}")
            # 寻找天气情况
            temp = re.findall(r'[A-Za-z]+\s?[A-Za-z]+', re.sub('\x1b.*?m', '', txt[11]))  # 12行是当天的天气
            # temp = re.sub('\x1b.*?m', '', txt[3]).split()
            if len(temp) < 4:
                return
            self.weather.setText(temp[0])
            self.weather_2.setText(temp[1])
            self.weather_3.setText(temp[2])
            self.weather_4.setText(temp[3])
            # 寻找温度情况
            temp = re.findall(r'[+-]?[0-9]+\([0-9]+\)', re.sub('\x1b.*?m', '', txt[12]))  # 13行是当天的温度
            if len(temp) < 4:
                return
            # self.weatherInfo.setText(f"{txt[2].strip()} {temp[-2]} {temp[-1]}")
            self.temper.setText(f"{temp[0]} ℃")
            self.temper_2.setText(f"{temp[1]} ℃")
            self.temper_3.setText(f"{temp[2]} ℃")
            self.temper_4.setText(f"{temp[3]} ℃")
        except requests.exceptions.RequestException or requests.exceptions.ConnectionError or \
                requests.exceptions.SSLError:
            pass

    def getIp(self):
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            ip = st.getsockname()[0]
        except socket.error:
            ip = '127.0.0.1'
        finally:
            st.close()
        self.ipInfo.setText(ip)

    def timerEvent(self, a0):
        self.timeInfo.setText(time.asctime(time.localtime()))
        self.getIp()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = LifeTool()
    # # ui = QtWebEngineWidgets.QWebEngineView()
    # # ui.load(QUrl('https://wttr.in/'))
    ui.show()
    sys.exit(app.exec_())
    # print(requests.get('http://www.weather.com.cn/data/sk').content.decode('utf-8'))
    # import requests
    # import json
    #
    # # url = "http://httpbin.org/ip"  # 也可以直接在浏览器访问这个地址
    # # r = requests.get(url)  # 获取返回的值
    # # ip = json.loads(r.text)["origin"]  # 取其中某个字段的值
    # # print(ip)
    #
    # url = 'https://wttr.in/'
    # r = requests.get(url).text.split('\n')
    # print(r[11])
    # print(re.findall(r'[A-Za-z]+\s?[A-Za-z]+', re.sub('\x1b.*?m', '', r[11])))
    # print(r[12])
