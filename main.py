# coding:utf-8

#  ----------------------------------------------------------------
# 设计逻辑：先在UI文件夹下新建自己的UI文件夹，后在pyqtdesigner里面设计好页面文件
# 而后实现控制逻辑，最后在本文件定义类，最后在window类中添加实例
# ----------------------------------------------------------------

import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme)
from qfluentwidgets import FluentIcon as FIF

# ----------------------------------------------------------------
# 在这里引入相关UI文件
from UI.object_detection import controlGwindow


# ----------------------------------------------------------------


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

# ----------------------------------------------------------------
# 在这里定义并继承自己写的控制逻辑页面，然后定义init方法，调用super().__init

class detectWidget(controlGwindow.detectionTab):
    def __init__(self):
        super().__init__()

# ----------------------------------------------------------------


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------------------
        # 在这里实例化页面，把widget替换成自己的实例
        # 图像处理
        self.ImageProcessingInterface = Widget('Image Processing', self)
        # 目标检测
        self.detectInterface = detectWidget()
        # 图像分割
        self.ImageSegmentationInterface = Widget('Image Segmentation', self)
        # 标志分类
        self.SignClassificationInterface = Widget('Sign Classification', self)
        # ----------------------------------------------------------------

        self.settingInterface = Widget('Settings', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.ImageProcessingInterface, FIF.PHOTO, 'Image Processing')
        self.addSubInterface(self.detectInterface, FIF.ZOOM, 'Object Detection')
        self.addSubInterface(self.ImageSegmentationInterface, FIF.TILES, 'Image Segmentation')
        self.addSubInterface(self.SignClassificationInterface, FIF.LABEL, 'Sign Classification')
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Traffic Sign Detection System')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # use custom background color theme (only available when the mica effect is disabled)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()