from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QLineEdit, QGraphicsDropShadowEffect, QLabel
import sys
from qtawesome import icon
from swqt.omulet import ShockwaveWidget, InputLineEdit, FuncButton, ElementGroup, FuncWidget, ShadowLabel, Button, \
    TitleLabel


class Main(FuncWidget):
    def __init__(self, size: QRect):
        super(Main, self).__init__(size)

        self.ll = ShadowLabel(QColor('dodgerblue'), 'left', 9, self, 0)
        self.ll.setGeometry(1, 0, 300, self.height())
        self.add_label(self.ll)

        self.g_btn = ElementGroup(self)

        self.a = FuncButton(self.g_btn, 'Memo', self.ll)
        self.b = FuncButton(self.g_btn, 'Diary', self.ll)
        self.c = FuncButton(self.g_btn, 'Day Plan', self.ll)
        self.d = FuncButton(self.g_btn, '+', self.ll)

        self.tl = TitleLabel(0, '', self.ll)
        self.tl.setText('GoalUp')
        self.tl.setGeometry(0, 0, 290, 60)

        self.tl2 = TitleLabel(0, '', self.l_bg)
        self.tl2.setGeometry(290, 0, 290, 60)
        self.tl2.lower()

        self.wa = QWidget(self)
        self.wb = QWidget(self)
        self.wc = QWidget(self)
        self.wd = QWidget(self)

        self.g_btn.addElements([self.a, self.b, self.c, self.d])

        self.a.set_widget(self.wa)
        self.b.set_widget(self.wb)
        self.c.set_widget(self.wc)
        self.d.set_widget(self.wd)

        self.a.setGeometry(0, 60, 290, 80)
        self.b.setGeometry(0, 140, 290, 80)
        self.c.setGeometry(0, 220, 290, 80)
        self.d.setGeometry(0, 300, 290, 80)

        self.wa.setGeometry(300, 80, 200, 200)
        self.wb.setGeometry(300, 80, 200, 200)
        self.wc.setGeometry(300, 80, 200, 200)
        self.wd.setGeometry(300, 80, 200, 200)


app = QApplication(sys.argv)
m = Main(app.desktop().screenGeometry())
m.show()
sys.exit(app.exec_())

# print([(x, y) for x in range(0, 5) for y in range(1, 3)])
# print(Qt.white)  # 3
