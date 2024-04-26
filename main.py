from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPen, QColor, QFont
import sys
import os
import shutil

from UI.MyMainWindow import Ui_MainWindow
from UI.object_detection import controlGwindow

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 在UI文件夹下面新建自己的文件夹，添加自己的页面和控制逻辑，一个控制逻辑，一个designer设计的页面文件
        # 把contorlGwindow.detectionTab()换成自己写的页面文件
        # 图像增强页
        self.tab02ui = QWidget()
        self.ui.tabWidget.addTab(self.tab02ui, "图像增强")

        # 目标检测页
        self.tab03ui = controlGwindow.detectionTab()
        self.ui.tabWidget.addTab(self.tab03ui,"目标检测")

        # 图像分割页
        self.tab04ui = QWidget()
        self.ui.tabWidget.addTab(self.tab04ui, "图像分割")

        # 标志分类页
        self.tab05ui = QWidget()
        self.ui.tabWidget.addTab(self.tab05ui, "标志识别")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
