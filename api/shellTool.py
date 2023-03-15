#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
源文件名: pshell.py
功能描述: 
作者: ShuJie
版本: V0.1
创建时间: 2023/3/13 19:46

修改历史: 
修改时间: 
版本号: 
修改人: 
修改内容: 
"""
# 库引入
import subprocess
import sys
import os

from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt, QTimer, QEvent
from PyQt5.QtGui import QTextCursor, QKeyEvent, QMouseEvent, QFocusEvent, QInputMethodEvent
from PyQt5.QtWidgets import QWidget, QApplication
from ui.pshell import Ui_pshell

# 变量声明
version = 0
subversion = 0
reversion = 1
# 函数定义
# def 
# 类定义


class EmitText(QObject):
    text = pyqtSignal(str)

    def write(self, string):
        self.text[str].emit(string)


class InfoThread(QThread):

    strSignal = pyqtSignal(str)

    def __init__(self):
        super(InfoThread, self).__init__()
        self.str = ''

    def setCmd(self, string):
        self.str = string

    def run(self):
        p = subprocess.Popen(self.str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while p.poll() is None:
            self.strSignal[str].emit(p.stdout.readline().decode('gbk'))
            if p.returncode is not None:
                break
        while p.poll() != 0:
            self.strSignal[str].emit(p.stderr.readline().decode('gbk'))
            if p.returncode is not None:
                break


class ShellTool(QWidget, Ui_pshell):
    """
    待定事件:
    1.当在输入位置按下回车, 会删除一个占位符, 偏离了无法删除既定输出的设定,
    2.当光标移动到不可删除区域, 会出现光标无法再出现《 这个问题由于对text内容进行只读设定造成, 后期看是否更换部分内容只读的方式
    """
    def __init__(self, parent=None, *args, **kwargs):

        super().__init__(parent)
        self.current = os.getcwd()
        self.currentPos = -1
        self.setupUi(self)
        self.th = InfoThread()
        self.th.finished.connect(self.shell)
        self.textCursor = self.textEdit.textCursor()
        self.connect()
        self.header()
        self.shell()

    def header(self):
        self.textEdit.setText(f'Py Shell [version {version}.{subversion}.{reversion}]\n'
                              '(C) Free Open Source\n'
                              'Remember That this shell just for command check, command like \'cd ..\' is void\n\n')

    def connect(self):
        self.textEdit.cursorPositionChanged.connect(self.onCursorMove)
        self.th.strSignal[str].connect(self.toText)

    def onCursorMove(self):
        if self.textEdit.textCursor().position() < self.currentPos:
            self.textEdit.setReadOnly(True)
            self.textEdit.setFocus()
        else:
            self.textEdit.setReadOnly(False)

        # print('pos', a)
        # print('block', b)
        # print('len', a - b)
        # print(self.textEdit.textCursor().block().layout().lineForTextPosition(a - b).lineNumber() +
        #       self.textEdit.textCursor().block().firstLineNumber())

    def shell(self):
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(self.current + '>>')
        self.textEdit.moveCursor(QTextCursor.End)
        # self.textEdit.setFocus(Qt.MouseFocusReason)
        self.currentPos = self.textEdit.textCursor().position()

    def getCmd(self):
        a = self.textEdit.toPlainText()[self.currentPos:]
        if a == '\n':
            self.shell()
            return
        self.th.setCmd(a)
        self.th.start()

    def toText(self, string):
        self.textEdit.insertPlainText(string)

    def keyReleaseEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Return:
            self.getCmd()
        return super(ShellTool, self).keyReleaseEvent(a0)

    # def event(self, a0: QEvent):
    #     print('type', a0.type())
    #     try:
    #         print('pos', self.textEdit.textCursor().position())
    #     except AttributeError:
    #         pass
    #     print('last', self.currentPos)
    #     if a0.type() == QEvent.KeyRelease and a0.key() == Qt.Key_Delete and self.textEdit.textCursor().position() == self.currentPos:
    #         print('yes')
    #         self.textEdit.setReadOnly(True)
    #         self.textEdit.setFocus()
    #         a0.ignore()
    #     return super(ShellTool, self).event(a0)

    # def eventFilter(self, a0: QObject, a1: QEvent):
    #     if a1.type() == QEvent.KeyRelease and


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = ShellTool()
    ui.show()

    sys.exit(app.exec_())
