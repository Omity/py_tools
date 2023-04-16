# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import os.path
import sys
import common.project_info as pi

from PyQt5.QtCore import QRegExp, QUrl
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QButtonGroup

from ui.ascii import Ui_ascii

ascii_control = [
    '\\0',
    'SOH',
    'STX',
    'ETX',
    'EOT',
    'ENQ',
    'ACK',
    '\\a',
    '\\b',
    '\\t',
    '\\n',
    '\\v',
    '\\f',
    '\\r',
    'SO',
    'SI',
    'DLE',
    'DC1',
    'DC2',
    'DC3',
    'DC4',
    'NAK',
    'SYN',
    'ETB',
    'CAN',
    'EM',
    'SUB',
    '\\e',
    'FS',
    'GS',
    'RS',
    'US',
    'SP',
    'DEL',
]


def asciiToNum(pString):
    """
    转换ascii为进制数
    :param pString: 需要转换的字符串
    :return: 以字典为单位的数组, 每个字典包含二进制、八进制、十进制和十六进制
    """
    temp = ['', '', '', '']
    for i in pString:
        if i != ' ':  # 非空格
            num = ord(i)  # 得到十进制数
            if num > 127:  # 超过范围
                return None
            temp[0] += bin(num).split('0b')[-1] + ' '   # 二进制
            temp[1] += oct(num).split('0o')[-1] + ' '   # 八进制
            temp[2] += str(num) + ' '                   # 十进制
            temp[3] += hex(num).split('0x')[-1] + ' '   # 十六进制
    return temp


def _numToAscii(num):
    """
    转换数字为ascii码
    :return:
    """
    if num > 127:  # ascii 范围0-127
        return 'NaN'
    elif num == 127:
        return ascii_control[-1]
    elif 0 < num < 32:
        return ascii_control[num]
    else:
        return chr(num)


def numToAscii(string, numType):
    """
    转换字符串为ascii
    :param string: 字符串
    :param numType: 字符串数字组成类型, 有2、8、10、16
    :return: 字符串组成的数组
    """
    result = ''
    temp = string.split()  # 以空格分隔
    for i in temp:
        result += _numToAscii(int(i, numType)) + ' '

    return result


class AsciiTool(QWidget, Ui_ascii):

    ASCII_TO_NUM = 0
    NUM_TO_ASCII = 1
    _bin_re = r'^[0-1\s]+$'
    _oct_re = r'^[0-7\s]+$'
    _dec_re = r'^[0-9\s]+$'
    _hex_re = r'^[a-fA-F0-9\s]+$'

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.group = QButtonGroup(self)
        self.numType = 3
        self.abspath = kwargs.get('path')
        self.setupUi(self)
        self.textBrowser.setSource(QUrl.fromLocalFile(os.path.join(self.abspath, f'{pi.DATA_FILE}/ascii_info.html')))

        self.transformChoiceItem = [
            self.asciiToNum,
            self.numToAscii
        ]
        self.numTypeItem = [
            [2, QRegExpValidator(QRegExp(self._bin_re), self)],
            [8, QRegExpValidator(QRegExp(self._oct_re), self)],
            [10, QRegExpValidator(QRegExp(self._dec_re), self)],
            [16, QRegExpValidator(QRegExp(self._hex_re), self)],
        ]
        self.connect()
        self.buttonGroup()
        self.choiceAsciiToNum.click()  # 默认启动ascii转数字
        self.numChoice.setCurrentIndex(self.numType)  # 数字默认16进制
        self.numEdit.setValidator(self.numTypeItem[self.numType][1])
        self.warningLabel.setStyleSheet('color:red;')

    def buttonGroup(self):
        self.group.addButton(self.choiceAsciiToNum, id=0)
        self.group.addButton(self.choiceNumToAscii, id=1)

    def connect(self):
        self.group.buttonClicked[int].connect(self.choiceChanged)
        self.asciiEdit.textEdited.connect(lambda: self.editInput(self.ASCII_TO_NUM))
        self.numEdit.textEdited.connect(lambda: self.editInput(self.NUM_TO_ASCII))
        self.numChoice.currentIndexChanged[int].connect(self.numTypeChanged)

    def choiceChanged(self, index):
        self.stackedWidget.setCurrentWidget(self.transformChoiceItem[index])

    def numTypeChanged(self, index):
        self.numType = index
        self.numEdit.setValidator(self.numTypeItem[index][1])
        self.editInput(self.NUM_TO_ASCII)

    def editInput(self, aType):
        if aType == self.ASCII_TO_NUM:
            self.warningLabel.clear()
            text = self.asciiEdit.text()
            out = asciiToNum(text)
            if out is None:
                self.warningLabel.setText('Invalid')
            else:
                self.binaryOut.setText(out[0])
                self.octonaryOut.setText(out[1])
                self.decimalOut.setText(out[2])
                self.hexadecimalOut.setText(out[3])
        elif aType == self.NUM_TO_ASCII:
            text = self.numEdit.text()
            out = numToAscii(text, self.numTypeItem[self.numType][0])
            self.asciiOut.setText(out)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AsciiTool(path='../')
    ui.setWindowIcon(QIcon(f'../{pi.DATA_FILE}/py_tool.ico'))
    ui.show()
    sys.exit(app.exec_())
