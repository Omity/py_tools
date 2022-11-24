#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名：conversionTool.py
功能描述：
作者：ShuJie
版本：V0.1
创建时间：2022/10/6 16:03

修改历史：
修改时间：
版本号：
修改人：
修改内容：
"""
# 库引入
import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QApplication, QButtonGroup
from conversion import Ui_conversion

# 变量声明
# G_para = '' 
# 函数定义


def conversionOfNum(string, numType):
    """
    转换进制
    :param string: 进制字符串
    :param numType: 进制类型
    :return: 四种进制结果
    """
    result = ['', '', '', '']
    temp = string.split()
    for i in temp:
        j = int(i, numType)
        result[0] += bin(j).split('0b')[-1] + ' '  # 二进制
        result[1] += oct(j).split('0o')[-1] + ' '  # 八进制
        result[2] += str(j) + ' '                  # 十进制
        result[3] += hex(j).split('0x')[-1] + ' '  # 十六进制

    return result

# 类定义


class ConversionTool(QWidget, Ui_conversion):
    _bin_re = r'^[0-1\s]+$'
    _oct_re = r'^[0-7\s]+$'
    _dec_re = r'^[0-9\s]+$'
    _hex_re = r'^[a-fA-F0-9\s]+$'

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.conversionItem = [
            ['0b', 2, QRegExpValidator(QRegExp(self._bin_re), self)],
            ['0o', 8, QRegExpValidator(QRegExp(self._oct_re), self)],
            ['0d', 10, QRegExpValidator(QRegExp(self._dec_re), self)],
            ['0x', 16, QRegExpValidator(QRegExp(self._hex_re), self)],
        ]
        self.numType = 3
        self.setupUi(self)
        self.group = QButtonGroup(self)
        self.add()
        self.connect()
        self.numChoice.setCurrentIndex(self.numType)
        self.numMask.setText(self.conversionItem[self.numType][0])
        self.numEdit.setValidator(self.conversionItem[self.numType][2])

    def add(self):
        self.group.addButton(self.binBtn, id=0)
        self.group.addButton(self.octBtn, id=1)
        self.group.addButton(self.intBtn, id=2)
        self.group.addButton(self.hexBtn, id=3)

    def connect(self):
        self.group.buttonClicked[int].connect(self.buttonClick)
        self.numChoice.currentIndexChanged[int].connect(self.numChoiceChanged)
        self.numEdit.textEdited.connect(lambda: self.editInput(self.conversionItem[self.numType][1]))

    def buttonClick(self, num):
        self.numChoice.setCurrentIndex(num)

    def numChoiceChanged(self, numType):
        self.numType = numType
        self.numMask.setText(self.conversionItem[numType][0])
        self.numEdit.setValidator(self.conversionItem[numType][2])

    def editInput(self, numType):
        string = self.numEdit.text()
        out = conversionOfNum(string, numType)
        self.lineEdit.setText(out[0])
        self.lineEdit_2.setText(out[1])
        self.lineEdit_3.setText(out[2])
        self.lineEdit_4.setText(out[3])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = ConversionTool()
    ui.show()

    sys.exit(app.exec_())
