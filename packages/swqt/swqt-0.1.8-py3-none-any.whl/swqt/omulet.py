# -*-coding:GBK -*-
import math
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QAction, QButtonGroup, QGraphicsDropShadowEffect
from PyQt5.QtCore import QThread, Qt, QPropertyAnimation, pyqtProperty, QPoint, QRect, QRectF
from PyQt5.QtGui import QColor, QIcon, QPalette, QPainterPath, QPainter, QBrush, QPen, QFont
from qtawesome import icon
import cgitb
from swqt.utils import *

cgitb.enable(format='text')

'''
pycharm会搜索sitepkg, 如果有文件夹就会生成自动补全，没有文件回跳转文件夹，
有__init__.py则跳转至该文件；其他文件夹需要设置成src文件夹才会添加至自动索引；同样的src文件夹有同名包冲突。优先级？
src 下面所有的作为python包名的文件夹都可以作为引用
pkg python包，文件夹名即为包名
开发python包可以开两个项目，在开发项目里设本地开发环境为src与pkg，测试项目里不需要，直接使用pip的包进行
测试
软件的灵魂需要优秀的美工
rgba() rgba值某一个超过了255，就是黑色
'''


# TODO: 标题label渐变色算法
# TODO: 对label进行贴边分类
# import 索引顺序: py文件名 --- 本文件夹包名 --- site pak包名
# TODO: 两种阴影的区别
# TODO: 鼠标边界捕捉不灵敏
# app.desktop().screenGeometry() 返回值
# TODO: resize时形状错位
# TODO: 鼠标形状错误
# TODO: 透明按钮，
# TODO： 自适应，全屏拽下来缩小一个分辨率等级,windows分屏适应
# TODO： Intro页，各种样式进度条
# windows统一窗体都有alt+space+X的控制方式
# 最小化变不回来的问题
# 某个事件触发了按钮的resize
# TODO: 阴影效果: paintEvent或者自身api
# TODO: 自定义软件布局
# TODO: 父子控件事件响应
# TODO: 边缘控件与缩放冲突

def fill_area(shadow_pos, step, w, h):
    if shadow_pos == 'full':
        return QRectF(step, step, w - step * 2, h - step * 2)
    if shadow_pos == 'left':
        return QRectF(0, 0, w - step, h)
    if shadow_pos == 'right':
        return QRectF(step, 0, w - step, h)
    if shadow_pos == 'up':
        return QRectF(0, 0, w, h - step)
    if shadow_pos == 'down':
        return QRectF(0, step, w, h - step)


def shadow_area(shadow_pos, step, i, w, h):
    if shadow_pos == 'full':
        return QRect(step - i, step - i, w - (step - i) * 2, h - (step - i) * 2)
    if shadow_pos == 'left':
        return QPoint(w - step + i, i), QPoint(w - step + i, h - i * 2)
    if shadow_pos == 'right':
        return QPoint(step - i, i), QPoint(step - i, h - i * 2)
    if shadow_pos == 'up':
        return QPoint(i, h - step + i), QPoint(w - i * 2, h - step + i)
    if shadow_pos == 'down':
        return QPoint(i, step - i), QPoint(w - i * 2, step - i)


def geo_pos(widget, event):
    g = widget.geometry()
    w = g.width()
    h = g.height()
    x = event.pos().x()
    y = event.pos().y()
    return g, w, h, x, y


class Button(QPushButton):
    def __init__(self, text='', p=None, ico=None):
        super(Button, self).__init__(text, p)

        if ico:
            self.setIcon(ico)

        self.setFont(QFont("Microsoft YaHei", 11, 75))
        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(245, 245, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(245, 245, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(Button, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(Button, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')


class CloseButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(CloseButton, self).__init__(text, p)

        self.setIcon(ico)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(255, 69, 0, 255))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(255, 69, 0, 255))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(CloseButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''background:mediumvioletred;border: 0 solid''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(CloseButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''background:orangered;border: 0 solid''')


class OtherButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(OtherButton, self).__init__(text, p)

        self.setIcon(ico)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(245, 245, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(245, 245, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(OtherButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(OtherButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')


class IntroWidget(QWidget):
    def __init__(self, parent=None):
        super(IntroWidget, self).__init__(parent)


class ShockwaveWidget(QWidget):
    def __init__(self, parent=None):
        super(ShockwaveWidget, self).__init__(parent)

        self.__startPos = None
        self.__endPos = None
        self.__isTracking = False

        self.l_bg = QLabel(self)

        self.btn_close = CloseButton(icon('fa.times', color='azure'), '', self)
        self.btn_mini = OtherButton(icon('fa.minus', color='azure'), '', self)
        self.btn_hint = OtherButton(icon('fa.chevron-down', color='azure'), '', self)

        self.__g_setting()
        self.__s_setting()
        self.__o_setting()

    def __g_setting(self):
        self.resize(500, 500)

        self.l_bg.setGeometry(0, 0, 500, 500)

    def __s_setting(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.l_bg.setStyleSheet('''background:lightblue''')

    def __o_setting(self):
        self.btn_close.clicked.connect(self.close)
        # obj.btn_close.clicked.connect(lambda: systemtrayicon('shutdown -s -t 5'))
        self.btn_mini.clicked.connect(self.showMinimized)

    def geometry_setting(self):
        pass

    def style_setting(self):
        pass

    def other_setting(self):
        pass

    def closeEvent(self, e):
        self.btn_close.setStyleSheet('''background:transparent''')
        self.btn_close.repaint()
        e.accept()

    def resizeEvent(self, e):
        w = self.geometry().width()

        self.l_bg.resize(self.size())

        self.btn_close.move(w - 40, 0)
        self.btn_mini.move(w - 80, 0)
        self.btn_hint.move(w - 120, 0)

    def mouseMoveEvent(self, e):
        try:
            self.__endPos = e.pos() - self.__startPos
            self.move(self.pos() + self.__endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = True
            self.__startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = False
            self.__startPos = None
            self.__endPos = None


class Separator(QLabel):
    def __init__(self):
        super(Separator, self).__init__()


class OmuCalender():
    def __init__(self):
        pass


class FuncLabel(QLabel):
    def __init__(self, adhere_pos, bg_color: str, p):
        super(FuncLabel, self).__init__(p)

        self.setMouseTracking(True)

        self.bg_color = QColor(bg_color)
        self.color_handle = 'rgba' + str((self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), 255))

        self.adhere_pos = adhere_pos

    def set_color(self):
        self.setStyleSheet('''background-color:%s''' % self.color_handle)


class TitleLabel(FuncLabel):
    def __init__(self, adhere_pos, bg_color: str, p: FuncLabel):
        super(TitleLabel, self).__init__(adhere_pos, bg_color, p)

        self.l_text = QLabel(self)
        self.l_text.setFont(QFont("Microsoft YaHei", 11, 75))

        if not bg_color:
            self.color_handle = 'rgba' + str((p.bg_color.red(), p.bg_color.green(), p.bg_color.blue(), 255))
        else:
            self.bg_color = QColor(bg_color)
            self.color_handle = 'rgba' + str((self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), 255))
        self.set_color()

    def set_color(self):
        self.setStyleSheet('''background-color:%s''' % self.color_handle)
        self.l_text.setStyleSheet('''background-color:transparent; color: rgb(197, 237, 226)''')

    def setText(self, text: str):
        self.l_text.setText(text)

    def resizeEvent(self, e):
        w = self.width()
        h = self.height()

        self.l_text.setGeometry(15, 5, w - 20, h - 20)


class ShadowLabel(FuncLabel):
    def __init__(self, bg_color, shadow_pos: str, step=5, p=None, adhere_pos=None):
        """
        shadow label for part or bg
        :param bg_color: 背景色
        :param mode: 1 component, 0 background
        :param shadow_pos: 位置, left, right, up, down
        :param step: 阴影层数
        :param p: parent
        """
        super(ShadowLabel, self).__init__(adhere_pos, bg_color, p)
        self.step = step
        self.position = shadow_pos

        self.effect_shadow = None
        if self.position == 'full':
            self.bg_shadow_setting()

    def bg_shadow_setting(self):
        self.set_color()
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(15)  # 阴影半径
        self.effect_shadow.setColor(Qt.darkGray)  # 阴影颜色
        self.setGraphicsEffect(self.effect_shadow)

    def paintEvent(self, e):
        if self.position != 'full':
            step = self.step
            w = self.width()
            h = self.height()

            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRect(fill_area(self.position, step, w, h))
            painter = QPainter(self)
            color = QColor(self.bg_color)
            color.setAlpha(255)
            painter.fillPath(path, QBrush(color))

            color = QColor(90, 90, 90, 30)
            # if self.position == 'full':
            #     for i in range(step):
            #         color.setAlpha(int(120 - math.sqrt(i) * 40))
            #         painter.setPen(QPen(color, 1, Qt.SolidLine))
            #         painter.drawRoundedRect(shadow_area(self.position, step, i, w, h), 1, 1)
            # else:
            for i in range(step):
                color.setAlpha(int(150 - math.sqrt(i) * 50))
                painter.setPen(QPen(color, 1, Qt.SolidLine))
                p1, p2 = shadow_area(self.position, step, i, w, h)
                painter.drawLine(p1, p2)


class FuncWidget(QWidget):
    def __init__(self, desktop_geo: QRect, parent=None):
        super(FuncWidget, self).__init__(parent)

        self.desktop_geo = desktop_geo

        self.old_geo = None

        self.__condition = 'max'

        self.__trigger_drag = False
        self.__bottom_drag = False
        self.__right_drag = False
        self.__left_drag = False
        self.__right_bottom_corner_drag = False
        self.__left_bottom_corner_drag = False

        self.__startPos = None
        self.__endPos = None
        self.__left_rect = None
        self.__right_rect = None
        self.__bottom_rect = None
        self.__right_bottom_corner_rect = None
        self.__left_bottom_corner_rect = None

        self.list_l = list()

        self.l_bg = ShadowLabel('lightskyblue', 'full', 5, self)

        self.btn_close = CloseButton(icon('fa.times', color='azure'), '', self)
        self.btn_mini = OtherButton(icon('fa.minus', color='azure'), '', self)
        self.btn_max_norm = OtherButton(icon('fa5.minus-square', color='azure'), '', self)

        self.__g_setting()
        self.__s_setting()
        self.__o_setting()

    def __g_setting(self):
        self.setGeometry(self.desktop_geo)

    def __s_setting(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.l_bg.setStyleSheet('''background-color: rgba(135,206,250,223)''')

    def __o_setting(self):
        self.setMouseTracking(True)
        self.l_bg.lower()

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.btn_max_norm.clicked.connect(self.normalize)

        self.btn_close.clicked.connect(self.close)
        # obj.btn_close.clicked.connect(lambda: systemtrayicon('shutdown -s -t 5'))
        self.btn_mini.clicked.connect(self.showMinimized)

    def geometry_setting(self):
        pass

    def style_setting(self):
        pass

    def other_setting(self):
        pass

    def add_label(self, label: QLabel):
        self.list_l.append(label)

    def normalize(self):
        self.__condition = 'normal'

        if self.old_geo:
            self.setGeometry(self.old_geo)
        else:
            self.resize(self.size() * 0.85)
        self.btn_max_norm.setIcon(icon('fa5.square', color='azure'))
        self.btn_max_norm.disconnect()
        self.btn_max_norm.clicked.connect(self.maximize)

    def maximize(self):
        self.__condition = 'max'
        self.old_geo = self.geometry()
        if self.old_geo.y() < 0:
            self.old_geo.setY(0)
        self.setGeometry(self.desktop_geo)
        self.btn_max_norm.setIcon(icon('fa5.minus-square', color='azure'))
        self.btn_max_norm.disconnect()
        self.btn_max_norm.clicked.connect(self.normalize)

    def closeEvent(self, e):
        self.btn_close.setStyleSheet('''background:transparent''')
        self.btn_close.repaint()
        e.accept()

    def moveEvent(self, e):
        if self.pos().y() > 0 and self.__condition == 'max':
            self.normalize()

    def mouseDoubleClickEvent(self, e):
        if self.geometry() != self.desktop_geo and self.size() != self.desktop_geo.size():
            self.maximize()
        else:
            self.normalize()

    def resizeEvent(self, e):
        g = self.geometry()
        w = g.width()
        h = g.height()

        old_pos = self.l_bg.pos()
        if g != self.desktop_geo:
            self.l_bg.setGeometry(5, 5, w - 10, h - 10)
            self.btn_close.move(w - 45, 5)
            self.btn_max_norm.move(w - 85, 5)
            self.btn_mini.move(w - 125, 5)
        else:
            self.l_bg.setGeometry(0, 0, w, h)
            self.btn_close.move(w - 40, 0)
            self.btn_max_norm.move(w - 80, 0)
            self.btn_mini.move(w - 120, 0)
        for label in self.list_l:
            label.move(label.pos() + self.l_bg.pos() - old_pos)
            if label.adhere_pos:
                label.resize(self.l_bg.width(), self.l_bg.height())
            else:
                label.resize(label.size().width(), self.l_bg.height())

    def mouseMoveEvent(self, e):
        g, w, h, x, y = geo_pos(self, e)
        if w - 10 <= w < w and h - 10 <= y <= h:
            self.setCursor(Qt.SizeFDiagCursor)
        elif 0 <= x < 10 and h - 10 <= y <= h:
            self.setCursor(Qt.SizeBDiagCursor)
        elif h - 10 <= y <= h and 10 < x < w - 10:
            self.setCursor(Qt.SizeVerCursor)
        elif (0 <= x < 10 or w - 10 <= x < w) and 50 < y < h - 10:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        if Qt.LeftButton and self.__right_drag:
            self.resize(x, h)
        elif Qt.LeftButton and self.__left_drag:
            self.resize(w - x, h)
            self.move(self.x() + x, self.y())
        elif Qt.LeftButton and self.__bottom_drag:
            self.resize(w, y)
        elif Qt.LeftButton and self.__right_bottom_corner_drag:
            self.resize(x, y)
        elif Qt.LeftButton and self.__left_bottom_corner_drag:
            self.resize(w - x, y)
            self.move(self.x() + x, self.y())
        elif Qt.LeftButton and self.__trigger_drag:
            self.__endPos = e.pos() - self.__startPos
            self.move(self.pos() + self.__endPos)

    def mousePressEvent(self, e):
        g, w, h, x, y = geo_pos(self, e)
        if e.button() == Qt.LeftButton and 10 <= x < w - 10 and 0 <= y <= 40:
            self.__trigger_drag = True
            self.__startPos = QPoint(x, y)
        elif w - 10 <= x < w and h - 10 <= y <= h:
            self.__right_bottom_corner_drag = True
        elif 0 <= x < 10 and h - 10 <= y <= h:
            self.__left_bottom_corner_drag = True
        elif 0 <= x < 10 and 50 < y < h - 10:
            self.__left_drag = True
        elif w - 10 <= x < w and 50 < y < h - 10:
            self.__right_drag = True
        elif h - 10 <= y <= h and 10 < x < w - 10:
            self.__bottom_drag = True

    def mouseReleaseEvent(self, e):
        self.__right_bottom_corner_drag = False
        self.__bottom_drag = False
        self.__right_drag = False
        self.__left_drag = False
        self.__left_bottom_corner_drag = False
        self.__trigger_drag = False
        self.__startPos = None
        self.__endPos = None
        if self.pos().y() < 0 and self.__condition == 'normal':
            self.maximize()


class InputLineEdit(QLineEdit):
    def __init__(self, parent=None, icon_name='', placeholder=''):
        super(InputLineEdit, self).__init__(parent)
        self.parent = parent
        self.cur = self.cursor()
        self.icon_name = icon_name

        self.setPlaceholderText(placeholder)

        self.action = QAction(self)
        self.action.setIcon(QIcon(icon('%s' % self.icon_name, color='silver')))
        self.addAction(self.action, QLineEdit.LeadingPosition)

        self.setStyleSheet('''
                            QLineEdit{
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 1px solid silver;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;
                                color:silver;} 
                            QLineEdit:hover {
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 2px solid silver;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;}''')

        self.setFocusPolicy(Qt.ClickFocus)

    def focusInEvent(self, e):
        super(InputLineEdit, self).focusInEvent(e)
        try:
            if self.parent.lw_login_record.current_state():
                lw_login_reverse(self.parent, 'hide')
        except:
            pass
        self.actions()[0].setIcon(QIcon(icon('%s' % self.icon_name, color='skyblue')))
        self.setStyleSheet('''
                            QLineEdit{
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 1px solid skyblue;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;}
                            ''')
        self.repaint()

    def focusOutEvent(self, e):
        inside_parent = self.parent.geometry().contains(self.cur.pos())
        if inside_parent:
            super(InputLineEdit, self).focusOutEvent(e)
            self.actions()[0].setIcon(QIcon(icon('%s' % self.icon_name, color='gray')))
            self.setStyleSheet('''
                                        QLineEdit{
                                            background: transparent;
                                            border: 0 solid;
                                            border-bottom: 1px solid silver;
                                            font-weight:bold;
                                            font-family: arial, serif;
                                            font-size:18px;
                                            color:silver;} 
                                        QLineEdit:hover {
                                            background: transparent;
                                            border: 0 solid;
                                            border-bottom: 2px solid silver;
                                            font-weight:bold;
                                            font-family: arial, serif;
                                            font-size:18px;}''')
            self.repaint()


class ElementGroup:
    def __init__(self, p=None):
        self.list_ele = list()

        self.__id_current_ele = 0
        self.num_ele = 0
        self.id_max_ele = 0

    # TODO: 只能加一次
    # TODO: 只能加FuncButton

    def get_current_id(self):
        return self.__id_current_ele

    def set_current_id(self, new_id):
        self.__id_current_ele = new_id

    def addElement(self, ele):
        self.id_max_ele += 1
        self.num_ele += 1
        ele.setWhatsThis(str(self.id_max_ele))
        self.list_ele.append(ele)

    def addElements(self, list_ele: list):
        for btn in list_ele:
            self.addElement(btn)

    # TODO: 内存搞鬼


class FuncButton(QPushButton):
    def __init__(self, group: ElementGroup, text='', p=None, ico=None):
        super(FuncButton, self).__init__(text, p)

        self.setFont(QFont("Microsoft YaHei", 11, 75))

        if ico:
            self.setIcon(ico)

        self.parent = p
        self.group = group
        self.is_checked = False

        self.widget = None

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(195, 195, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(195, 195, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

        self.clicked.connect(self.group_effect)

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def set_widget(self, widget):
        self.widget = widget

    def group_effect(self):
        if self.group.get_current_id():
            self.group.list_ele[self.group.get_current_id() - 1].uncheck()
        self.group.set_current_id(int(self.whatsThis()))
        self.group.list_ele[self.group.get_current_id() - 1].check()

    def check(self):
        self.is_checked = True
        self.widget.show()
        self.setStyleSheet('''background-color: rgba(240, 255, 220, 195); border: 0px solid''')

    def uncheck(self):
        self.is_checked = False
        self.widget.hide()
        self.setStyleSheet('''background: transparent; border: 0px solid''')

    def enterEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        super(FuncButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        super(FuncButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')
