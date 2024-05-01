from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsTextItem, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPen,QColor,QFont
import sys

from PyQt5.uic.properties import QtCore

from segWindow import Ui_Form
from Model.detect_model.yolo8 import yolo8
from Model.seg_model.deeplab import test_img
from Model.seg_model.Histogram import Histogram_bimodal
from Model.seg_model.K_means import K_means
import imagecut
import Model.seg_model.deeplab
from Model.detect_model.faster_rcnn import Faster_Rcnn
from Model.detect_model.my_yolo import myyolo


class segmentionTab(QWidget,Ui_Form):
    def __init__(self,callback=None):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.imgpath = ""
        self.imagePath_2 = ""
        self.imagePaths = []
        self.callback = callback
        self.boxes = []


        self.pushButton.clicked.connect(self.segmentionImg)
        self.ModelcomboBox.currentIndexChanged.connect(self.on_model_change)

        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.scene_2 = QGraphicsScene(self)
        self.graphicsView_2.setScene(self.scene_2)

        self.rectangles = []
        self.model = test_img

        self.pen = QPen()
        self.pen.setColor(Qt.red)
        self.pen.setWidth(10)

        self.judge_index = 0

        self.modellist = [ "Yolov8", "Deeplabv3", "Histogram_bimodal", "K_means"]
        for model in self.modellist:
            self.ModelcomboBox.addItem(model)
        self.ModelcomboBox.setCurrentIndex(0)

    def on_model_change(self,index):
        print(index)
        if index == 0:
            self.model = imagecut
        elif index == 1:
            self.model = test_img
        elif index == 2:
            self.model = Histogram_bimodal
        elif index == 3:
            self.model = K_means
        else:
            self.model = test_img
        self.judge_index = index
        print("model change to ",self.modellist[index])

    def dragEnterEvent(self, event):
        if self.scene is not None:
            self.scene.clear()
        print("dragEnterEvent")
        if event.mimeData().hasUrls():
            event.accept()
            print("accepting")
        else:
            event.ignore()
            print("ignored")

    def dropEvent(self, event):
        print("dropEvent")
        if event.mimeData().hasUrls():
            print("accepting")
            event.setDropAction(Qt.CopyAction)
            event.accept()

            self.imgpath = event.mimeData().urls()[0].toLocalFile()
            print(self.imgpath)
            self.imgPathChange(self.imgpath)
            # if self.callback:
            #     self.callback(self.imgpath)
            #     print("callback...")
            # print(self.imgpath)
            # self.imgdraw()

        else:
            event.ignore()
            print("ignored")

    def imgdraw(self):
        pixmap = QPixmap(self.imgpath)
        self.pixmapItem = self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        # self.remove_rectangle(self.scene)

    def imgPathChange(self,imgpath):
        self.imgpath = imgpath
        self.imgdraw()
        print(self.imgpath)



    def segmentionImg(self):
        print("imgupdate")
        clear_graphics_view(self)
        if self.judge_index == 0:  # yolov8
            print("1")
            self.imagePath_2 = self.model.save_cutImg(self.imgpath,self.boxes)

            if self.callback:
                self.callback()
                # print("callback...")
            print("imagePath = " + self.imagePath_2)
            # 创建一个QGraphicsScene对象
            pixmap = QPixmap(self.imagePath_2)
            # 将QPixmap添加到QGraphicsScene
            self.pixmapItem_2 = self.scene_2.addPixmap(pixmap)
            # 将QGraphicsScene设置到QGraphicsView
            # 适配图像大小
            self.graphicsView_2.fitInView(self.pixmapItem_2, Qt.KeepAspectRatio)
        elif self.judge_index == 1:   # deeplabv3
            # resultBox = self.model.segmentionfunc(self.imgpath)
            self.imagePath_2 = self.model.save_Image(self.imgpath)
            print("imagePath = " + self.imagePath_2)
            # 创建一个QGraphicsScene对象
            pixmap = QPixmap(self.imagePath_2)
            # 将QPixmap添加到QGraphicsScene
            self.pixmapItem_2 = self.scene_2.addPixmap(pixmap)
            # 将QGraphicsScene设置到QGraphicsView
            # 适配图像大小
            self.graphicsView_2.fitInView(self.pixmapItem_2, Qt.KeepAspectRatio)
        elif self.judge_index == 2:  # Histogram_bimodal
            # resultBox = self.model.segmentionfunc(self.imgpath)
            self.imagePaths = self.model.use_Histogram_bimodal(self.imgpath)
            self.imagePath_2 = self.imagePaths[-1]
            print("imagePath = " + self.imagePath_2)
            # 创建一个QGraphicsScene对象
            pixmap = QPixmap(self.imagePath_2)
            # 将QPixmap添加到QGraphicsScene
            self.pixmapItem_2 = self.scene_2.addPixmap(pixmap)
            # 将QGraphicsScene设置到QGraphicsView
            # 适配图像大小
            self.graphicsView_2.fitInView(self.pixmapItem_2, Qt.KeepAspectRatio)
            # self.imagePaths = self.model.use_Histogram_bimodal(self.imgpath)
            # # 创建QPixmap对象并添加到场景中
            # pixmapItems = []
            # total_height = 0  # 用于计算总高度，以便适配视图
            # for i, imagePath in enumerate(self.imagePaths):
            #     pixmap = QPixmap(imagePath)
            #     pixmapItem = self.scene_2.addPixmap(pixmap)
            #     pixmapItems.append(pixmapItem)
            #
            #     # 根据图片的高度和间隔调整每张图片的位置
            #     if i > 0:
            #         previous_pixmap_item = pixmapItems[i - 1]
            #         offset_y = previous_pixmap_item.boundingRect().height() + 10  # 10为两张图片之间的间隔
            #         pixmapItem.setPos(0, previous_pixmap_item.pos().y() + offset_y)
            #         total_height += offset_y
            #
            # # 更新总高度以包括最后一张图片的高度
            # total_height += pixmapItems[-1].boundingRect().height()
            #
            # # 将QGraphicsScene设置到QGraphicsView
            # self.graphicsView_2.setScene(self.scene_2)
            #
            # # 适配图像大小
            # self.graphicsView_2.fitInView(self.pixmapItem_2, Qt.KeepAspectRatio)
        elif self.judge_index == 3:  # K-means
            # resultBox = self.model.segmentionfunc(self.imgpath)
            self.imagePath_2 = self.model.use_K_means(self.imgpath)
            print("imagePath = " + self.imagePath_2)
            # 创建一个QGraphicsScene对象
            pixmap = QPixmap(self.imagePath_2)
            # 将QPixmap添加到QGraphicsScene
            self.pixmapItem_2 = self.scene_2.addPixmap(pixmap)
            # 将QGraphicsScene设置到QGraphicsView
            # 适配图像大小
            self.graphicsView_2.fitInView(self.pixmapItem_2, Qt.KeepAspectRatio)


def clear_graphics_view(self):
    if self.scene_2 is not None:
        self.scene_2.clear()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.segmtionTab = segmentionTab()
        self.tab1 = QTabWidget()

        self.tab_widget.addTab(self.segmtionTab, "Segmention")

        self.setCentralWidget(self.tab_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.resize(1200, 800)
    # tab = detectionTab()
    # MainWindow.setCentralWidget(tab)
    MainWindow.show()
    sys.exit(app.exec_())