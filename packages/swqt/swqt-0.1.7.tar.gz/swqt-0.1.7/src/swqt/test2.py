#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPalette
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QVBoxLayout,
        QWidget)


class WigglyWidget(QWidget):
    def __init__(self, parent=None):
        super(WigglyWidget, self).__init__(parent)

        self.setBackgroundRole(QPalette.Midlight)
        self.setAutoFillBackground(True)

        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QBasicTimer()
        self.text = ''

        self.step = 0;
        self.timer.start(60, self)

    def paintEvent(self, event):
        sineTable = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)

        metrics = QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QColor()

        painter = QPainter(self)

        for i, ch in enumerate(self.text):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)

    def setText(self, newText):
        self.text = newText

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            self.update()
        else:
            super(WigglyWidget, self).timerEvent(event)


class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        wigglyWidget = WigglyWidget()
        lineEdit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(wigglyWidget)
        layout.addWidget(lineEdit)
        self.setLayout(layout)

        lineEdit.textChanged.connect(wigglyWidget.setText)

        lineEdit.setText("Hello world!")

        self.setWindowTitle("Wiggly")
        self.resize(360, 145)

# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class WindowDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(WindowDemo, self).__init__()
        self.setup_ui()
        self.add_shadow()

    def setup_ui(self):
        self.setWindowOpacity(0.93)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.setFixedSize(300, 400)

        self.base_widget = QtWidgets.QWidget()  # 创建透明窗口
        self.base_widget.setStyleSheet('''QWidget{  border-radius:7px;background-color:rgb(255, 255, 255);}''')
        self.base_widget.setObjectName('base_widget')
        self.base_layout = QtWidgets.QGridLayout()
        self.base_widget.setLayout(self.base_layout)
        self.base_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setStyleSheet('''QWidget{border-radius:7px;background-color:rgb(255,255,255);}''')

        self.base_layout.addWidget(self.main_widget)

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

    def add_shadow(self):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = WindowDemo()
    dialog.show()
    sys.exit(app.exec_())