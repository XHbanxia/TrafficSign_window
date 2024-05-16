import time

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsTextItem, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPen,QColor,QFont

from Gviewwindow import Ui_Form
from Model.detect_model.yolo8 import yolo8
from Model.detect_model.faster_rcnn import Faster_Rcnn
from Model.detect_model.my_yolo import myyolo


class detectionTab(QWidget,Ui_Form):
    def __init__(self,callback=None,callback2=None):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.imgpath = ""
        self.callback = callback
        self.callback2 = callback2
        self.resultBox = []

        self.pushButton.clicked.connect(self.imgpredect)
        self.ModelcomboBox.currentIndexChanged.connect(self.on_model_change)

        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        self.rectangles = []
        self.Yolo8 = yolo8
        self.Faster_Rcnn = Faster_Rcnn
        self.myyolo = myyolo

        self.model = self.Faster_Rcnn



        self.pen = QPen()
        self.pen.setColor(Qt.red)
        self.pen.setWidth(10)

        self.modellist = ["Faster R-CNN", "Yolo8", "Tra-Yolo"]
        for model in self.modellist:
            self.ModelcomboBox.addItem(model)
        self.ModelcomboBox.setCurrentIndex(0)

    def on_model_change(self,index):
        # print(index)
        if index == 0:
            self.model = self.Faster_Rcnn
        elif index == 1:
            self.model = self.Yolo8
        elif index == 2:
            self.model = self.myyolo
        else:
            self.model = self.Faster_Rcnn
        self.remove_rectangle(self.scene)
        print("model load is ",self.modellist[index])

    def dragEnterEvent(self, event):
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
            if self.callback:
                self.callback(self.imgpath)
                print("callback...")
            self.imgPathChange(self.imgpath)
            # print(self.imgpath)
            # self.imgdraw()

        else:
            event.ignore()
            print("ignored")

    def imgdraw(self):
        self.label.setStyleSheet("font-size: 12pt")
        self.label.setText("结果显示框")
        self.remove_rectangle(self.scene)
        pixmap = QPixmap(self.imgpath)
        if self.scene is not None:
            self.scene.clear()
        self.pixmapItem = self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(self.pixmapItem, Qt.KeepAspectRatio)


    def imgPathChange(self,imgpath):
        self.imgpath = imgpath
        self.imgdraw()
        # print(self.imgpath)


    def imgpredect(self):
        # print("imgupdate")
        self.resultBox,prdictime= self.model.prodectfunc(self.imgpath)

        if self.callback2:
            self.callback2(self.resultBox)
        print("predict over")
        tempstr = "预测结果  \n序号     X     Y    W     H  \n"

        label = 0
        for box in self.resultBox:
            # print(box[0], box[1], box[2], box[3])
            self.add_rectangle(self.scene, box[0], box[1], box[2], box[3], label)
            # tempstr += "  " + str(label) + ",    " + str(int(box[0])) + ",  " + str(int(box[1])) + ",  " + str(
            #     int(box[2])) + ",  " + str(int(box[3])) + "\n"
            tempstr += f"{label:^6}{int(box[0]):^6}{int(box[1]):^6}{int(box[2]):^6}{int(box[3]):^6}\n"

            # print(tempstr)
            label += 1

        tempstr += f"\n\n预测花费时间：{prdictime:>5}ms"

        self.label.setStyleSheet("font-size: 18pt")
        self.label.setText(tempstr)

    def add_rectangle(self,scene,x,y,w,h,label_number):
        # 创建矩形框并添加到场景和列表中
        rex,rey = x-w/2,y-h/2
        rect_item = QGraphicsRectItem(int(rex), int(rey), int(w), int(h))
        rect_item.setPen(self.pen)
        scene.addItem(rect_item)
        self.rectangles.append(rect_item)

        text_item = QGraphicsTextItem(str(label_number))
        text_item.setPos(int(rex), int(rey))  # 设置文本位置为矩形框的左上角
        text_item.setDefaultTextColor(QColor('black'))  # 设置文本颜色为白色
        font = QFont()
        font.setPointSize(50)  # 设置字体大小
        font.setBold(True)
        text_item.setFont(font)  # 设置文本字体和大小
        scene.addItem(text_item)  # 将文本标签添加到场景中
        self.rectangles.append(text_item)


    def remove_rectangle(self,scene):
        # 从场景和列表中移除矩形框
        self.label.setStyleSheet("font-size: 12pt")
        self.label.setText("结果显示框")
        if self.rectangles:
            for re in self.rectangles:
                # print("remove")
                scene.removeItem(re)
                # print("removed..")
            self.rectangles = []



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        self.detectTab = detectionTab()
        self.tab1 = QTabWidget()

        self.tab_widget.addTab(self.detectTab, "Detection")

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