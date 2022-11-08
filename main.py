#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：main.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/10/6 20:47

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""
# 库引入

import sys
import ctypes

from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QWidget
from pytools import Ui_pyTools
from asciiTool import AsciiTool
from conversionTool import ConversionTool
from serialTool import SerialTool

# 变量声明
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PY TOOLS')
# 函数定义
# def 
# 类定义


class PyTools(QWidget, Ui_pyTools):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('PY TOOLS')
        self.setWindowIcon(QIcon('py_tool.ico'))

        self.animation = QPropertyAnimation(self, b"pos", self)

        self.ascii = AsciiTool(self)
        self.conversion = ConversionTool(self)
        self.serial = SerialTool(self)

        self.buttonItem = [
            self.ascii,
            self.conversion,
            self.serial
        ]

        self.stackedWidget.addWidget(self.ascii)
        self.stackedWidget.addWidget(self.conversion)
        self.stackedWidget.addWidget(self.serial)

        self.buttonGroup = QButtonGroup(self)
        self.buttonAdd()
        self.connect()
        self.asciiBtn.click()

    def connect(self):
        self.buttonGroup.buttonClicked[int].connect(self.buttonChanged)

    def buttonAdd(self):
        self.buttonGroup.addButton(self.asciiBtn, id=0)
        self.buttonGroup.addButton(self.conversionBtn, id=1)
        self.buttonGroup.addButton(self.serialBtn, id=2)

    def buttonChanged(self, index):
        self.stackedWidget.setCurrentWidget(self.buttonItem[index])

    def enterEvent(self, a0):
        if -10 - self.frameGeometry().height() <= self.y() <= -self.frameGeometry().height() + 10:
            animation = QPropertyAnimation(self, b"pos", self)
            animation.setStartValue(QPoint(self.x(), self.y()))
            animation.setEndValue(QPoint(self.x(), 0))
            animation.setDuration(200)
            animation.start()

    def leaveEvent(self, a0):
        if self.y() <= 2 and QCursor.pos().y() > self.frameGeometry().height() - self.geometry().height():
            animation = QPropertyAnimation(self, b"pos", self)
            animation.setStartValue(QPoint(self.x(), self.y()))
            animation.setEndValue(QPoint(self.x(),  2 - self.frameGeometry().height()))
            animation.setDuration(200)
            animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = PyTools()
    ui.show()

    sys.exit(app.exec_())
