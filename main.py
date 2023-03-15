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
import os.path
import sys
import ctypes

from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QPushButton, QSpacerItem, QSizePolicy
from ui.pytools import Ui_pyTools
from api.asciiTool import AsciiTool
from api.conversionTool import ConversionTool
from api.serialTool import SerialTool
from api.shellTool import ShellTool

# 变量声明
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PY TOOLS')
abs_path = os.path.dirname(__file__)
# 函数定义
# def 
# 类定义


class PyTools(QWidget, Ui_pyTools):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('PY TOOLS')
        self.setWindowIcon(QIcon(os.path.join(abs_path, 'data/py_tool.ico')))

        self.animation = QPropertyAnimation(self, b"pos", self)

        # UI
        self._widgetCreat()
        # 按键
        self._buttonCreat()

        self.buttonItem = []

        self.buttonGroup = QButtonGroup(self)

        self.addChild()
        self.connect()
        self.buttonGroup.button(0).click()

    def addNewWidget(self, widget, btn, idx):
        """
        添加按钮和对应的UI控件到主UI
        :param widget: UI对象
        :param btn: 按键对象
        :param idx: 按键索引
        :return:
        """
        # 管理UI数组
        self.buttonItem.append(widget)
        # 管理按键
        self.buttonGroup.addButton(btn, id=idx)
        # UI添加
        self.stackedWidget.addWidget(widget)
        # 按键添加
        self.gridLayout.addWidget(btn, idx, 0)

    def addChild(self):
        self.addNewWidget(self.ascii, self.asciiBtn, 0)
        self.addNewWidget(self.conversion, self.conversionBtn, 1)
        self.addNewWidget(self.serial, self.serialBtn, 2)
        self.addNewWidget(self.shell, self.shellBtn, 3)
        spacerItem = QSpacerItem(20, 40, vPolicy=QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem)

    def connect(self):
        self.buttonGroup.buttonClicked[int].connect(self.buttonChanged)

    def _widgetCreat(self):
        # 子UI
        self.ascii = AsciiTool(self, path=abs_path)
        self.conversion = ConversionTool(self)
        self.serial = SerialTool(self)
        self.shell = ShellTool(self)

    def _buttonCreat(self):
        """
        增加按键控制UI切换
        :return:
        """
        self.asciiBtn = QPushButton('ASCII')
        self.conversionBtn = QPushButton('CONVERSION')
        self.serialBtn = QPushButton('SERIAL')
        self.shellBtn = QPushButton('SHELL')

        self.asciiBtn.setCursor(Qt.PointingHandCursor)
        self.conversionBtn.setCursor(Qt.PointingHandCursor)
        self.serialBtn.setCursor(Qt.PointingHandCursor)
        self.shellBtn.setCursor(Qt.PointingHandCursor)

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
