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
from time import sleep

import common.project_info as pi
import common.version as ver

from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt, QThread, pyqtSignal, QObject, QMutex
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QPushButton, QSpacerItem, QSizePolicy, QDialog, \
    QGraphicsOpacityEffect
from ui.pytools import Ui_pyTools
from ui.upgrade import Ui_upgrade
from api.asciiTool import AsciiTool
from api.conversionTool import ConversionTool
from api.serialTool import SerialTool
from api.shellTool import ShellTool
from api.update import ProjectUpdate
from api.lifeTool import LifeTool

# 变量声明
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(pi.APP_NAME)
abs_path = os.path.dirname(os.path.abspath(__file__))
# 函数定义


def workflow_test():
    argv = sys.argv
    if len(argv) == 2:
        if argv[1] == 'test':
            print('app run success')
            sys.exit(0)
# 类定义


class UpdateThread(QThread):

    idle = 0
    check = 1
    download = 2

    upgrade_valid = 0
    upgrade_complete = 1

    validSignal = pyqtSignal(int)
    infoSignal = pyqtSignal(str)
    intSignal = pyqtSignal(int)

    def __init__(self, server, temp, zipFile, version=None, *args, **kwargs):
        super(UpdateThread, self).__init__()
        if version is None:
            version = []
        self.update = ProjectUpdate(server, callback=self.process)
        self.version = version
        self.tempDir = temp
        self.zip = zipFile
        self.lock = QMutex()
        self.size = 0
        self.state = self.idle

    def setState(self, state):
        self.lock.lock()
        self.state = state
        self.lock.unlock()

    def process(self, size):
        info = f'\tdownloading {round(self.size / 1024 / 1024, 2)}MB of {round(self.update.size / 1024 / 1024, 2)}MB'
        self.infoSignal[str].emit(info)
        self.size += size
        self.intSignal[int].emit(int(self.size / self.update.size * 100))

    def clear(self):
        self.size = 0
        self.setState(self.idle)

    def run(self):
        while True:
            if self.state == self.idle:
                continue
            elif self.state == self.check:
                if not self.update.isVersionBehind(self.version):
                    self.infoSignal[str].emit('your software is up to date')
                else:
                    self.infoSignal[str].emit(self.update.getUpdateInfo().strip('\n'))
                    self.validSignal[int].emit(self.upgrade_valid)
                self.setState(self.idle)
            elif self.state == self.download:
                self.update.downloadPack(self.zip, self.tempDir)
                self.validSignal[int].emit(self.upgrade_complete)
                self.clear()


class Upgrade(QDialog, Ui_upgrade):

    _close_valid = 0
    _upgrade_valid = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('upgrade')
        self.setWindowModality(Qt.ApplicationModal)
        self.effect = QGraphicsOpacityEffect()
        self.showProcess(False)
        server = f"{pi.PROJECT_SERVER}/{pi.PROJECT_AUTHOR}/{pi.PROJECT_NAME}"
        tempDir = os.path.join(abs_path, pi.PROJECT_UPDATE_DIR)
        self.version = [ver.VERSION_MAIN, ver.VERSION_SUB, ver.VERSION_FIX]
        self.updateThread = UpdateThread(server, tempDir, pi.PROJECT_UPDATE_FILE, version=self.version)
        self.updateThread.infoSignal[str].connect(self.write)
        self.updateThread.validSignal[int].connect(self.setButtonState)
        self.updateThread.intSignal[int].connect(self.updateProcess)
        self.pushButton.clicked.connect(self.buttonClick)
        self.state = False
        self.setButtonState(self.updateThread.upgrade_complete)

    def setButtonState(self, state):
        if state > self.updateThread.upgrade_complete:
            return
        if state == self.updateThread.upgrade_complete:
            self.pushButton.setDisabled(False)
            self.pushButton.setText('知道了')
            self.state = False
        elif state == self.updateThread.upgrade_valid:
            self.pushButton.setText('立即更新')
            self.state = True

    def buttonClick(self):
        if not self.state:
            self.close()
        else:
            self.showProcess(True)
            self.pushButton.setDisabled(True)
            self.updateThread.setState(self.updateThread.download)

    def write(self, info):
        self.infoText.clear()
        self.infoText.insertPlainText(info)

    def showProcess(self, show: bool):
        if show:
            self.effect.setOpacity(1)
            self.process.setGraphicsEffect(self.effect)
        else:
            self.effect.setOpacity(0)
            self.process.setGraphicsEffect(self.effect)

    def show(self):
        super(Upgrade, self).show()
        # self._threadRestore()
        self.write('\t\tchecking...')
        # print(self.updateThread)
        self.updateThread.start()
        self.updateThread.setState(self.updateThread.check)

    def updateProcess(self, cur):
        self.process.setValue(cur)

    def closeEvent(self, a0):
        self.showProcess(False)
        self.process.setValue(0)
        self.setButtonState(self._close_valid)
        return super(Upgrade, self).closeEvent(a0)


class PyTools(QWidget, Ui_pyTools):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle(f"{pi.APP_NAME} {ver.PROJECT_VERSION}")
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
        self.gridLayout_3.addWidget(self.life)
        self.buttonGroup.addButton(self.test, id=4)
        self.gridLayout.addWidget(self.test, 4, 0)
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
        self.upgrade = Upgrade(self)
        self.life = LifeTool(self)

    def _buttonCreat(self):
        """
        增加按键控制UI切换
        :return:
        """
        self.asciiBtn = QPushButton('ASCII')
        self.conversionBtn = QPushButton('CONVERSION')
        self.serialBtn = QPushButton('SERIAL')
        self.shellBtn = QPushButton('SHELL')
        self.test = QPushButton('test')

        self.asciiBtn.setCursor(Qt.PointingHandCursor)
        self.conversionBtn.setCursor(Qt.PointingHandCursor)
        self.serialBtn.setCursor(Qt.PointingHandCursor)
        self.shellBtn.setCursor(Qt.PointingHandCursor)
        self.test.setCursor(Qt.PointingHandCursor)

    def buttonChanged(self, index):
        if index == 4:
            self.upgrade.show()
        else:
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

    def show(self):
        workflow_test()
        return super(PyTools, self).show()


if __name__ == '__main__':
    workflow_test()
    app = QApplication(sys.argv)

    ui = PyTools()
    # ui = Upgrade()
    ui.show()

    sys.exit(app.exec_())
