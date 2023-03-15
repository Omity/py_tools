#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：serialTool.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/11/8 21:13

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""
# 库引入
import sys

import serial
import serial.tools.list_ports as lp
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem
from ui.serial_tool import Ui_serial_tool

# 变量声明
# G_para = '' 
# 函数定义


def checkPort():
    info = []
    p = lp.comports()
    for i in p:
        tmp = {
            'name': i.name,
            'description': i.description,
            'pid': i.pid,
            'vid': i.vid,
            'number':i.serial_number,
            'status': True
        }
        try:
            serial.Serial(i.device, 9600, timeout=10)
        except serial.SerialException:
            tmp['status'] = False
        info.append(tmp)
    return info


# 类定义


class SerialTool(QWidget, Ui_serial_tool):

    _TimerTime = 500

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setupUi(self)
        self.info = [
            {'name': 'com1', 'status': True, 'pid': 1, 'vid': 2, 'description': " test for o"}
        ]

        self.tableWidget.horizontalHeader().setSectionsClickable(False)  # 表头无法点击
        self.tableWidget.setShowGrid(False)  # 无外框
        self.tableWidget.setFocusPolicy(Qt.NoFocus)

        self.insert(self.info)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getPort)
        self.timer.start(self._TimerTime)

    def clear(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def insert(self, info):
        if not info:
            return
        for i in info:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            col0 = QTableWidgetItem(i['name'])
            if i['status']:
                col1 = QTableWidgetItem('useful')
                col1.setBackground(QColor(0, 255, 0))
            else:
                col1 = QTableWidgetItem('occupied')
                col1.setBackground(QColor(255, 0, 0))
            col2 = QTableWidgetItem(str(i['pid']))
            col3 = QTableWidgetItem(str(i['vid']))
            col4 = QTableWidgetItem(i['description'])
            col0.setTextAlignment(Qt.AlignCenter)
            col1.setTextAlignment(Qt.AlignCenter)
            col2.setTextAlignment(Qt.AlignCenter)
            col3.setTextAlignment(Qt.AlignCenter)
            col4.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(row, 0, col0)
            self.tableWidget.setItem(row, 1, col1)
            self.tableWidget.setItem(row, 2, col2)
            self.tableWidget.setItem(row, 3, col3)
            self.tableWidget.setItem(row, 4, col4)

    def getPort(self):
        self.timer.stop()
        info = checkPort()
        if info != self.info:
            self.info = info
            self.clear()
            self.insert(self.info)
        self.timer.start(self._TimerTime)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    print(checkPort())
    ui = SerialTool()
    ui.show()

    sys.exit(app.exec_())
