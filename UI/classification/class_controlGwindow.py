from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGraphicsScene, QGraphicsRectItem, \
    QGraphicsTextItem, QTabWidget, QHeaderView, QTableView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPen, QColor, QFont, QStandardItemModel, QStandardItem
import sys

from pyqt5_plugins.examplebutton import QtWidgets

from ClassGviewwindow import Ui_Form
from Model.classification_model.yolov8.yolov8 import Yolo8Original
from Model.classification_model.alexnet.alexnet import MyAlexNet
from Model.classification_model.MobileViT.MobileVit import MyMobileVit
import os

script_path = os.path.abspath(__file__)
script_dir_1 = os.path.dirname(script_path)
# print(script_dir_1)
class detectionTab(QWidget, Ui_Form):
    def __init__(self, image_paths):
        super().__init__()
        # 创建三种模型
        self.yoloModel = Yolo8Original()
        self.alexNet = MyAlexNet()
        self.mobileVit = MyMobileVit()
        self.nameMap = {
            "type_0": "限速5km/h",
            "type_1": "限速15km/h",
            "type_2": "限速30km/h",
            "type_3": "限速40km/h",
            "type_4": "限速50km/h",
            "type_5": "限速60km/h",
            "type_6": "限速70km/h",
            "type_7": "限速80km/h",
            "type_8": "禁止直行和左转",
            "type_9": "禁止直行和右转",
            "type_10": "禁止直行",
            "type_11": "禁止左转",
            "type_12": "禁止向左向右转弯",
            "type_13": "禁止右转",
            "type_14": "禁止超车",
            "type_15": "禁止掉头",
            "type_16": "禁止机动车通行",
            "type_17": "静止鸣笛",
            "type_18": "解除限速40km/h",
            "type_19": "解除限速50km/h",
            "type_20": "直行和向右转弯",
            "type_21": "直行",
            "type_22": "向左转弯",
            "type_23": "向左和向右转弯",
            "type_24": "向右转弯",
            "type_25": "靠左侧道路行驶",
            "type_26": "靠右侧道路行驶",
            "type_27": "环岛行驶",
            "type_28": "机动车行驶",
            "type_29": "鸣笛",
            "type_30": "非机动车行驶",
            "type_31": "允许鸣笛",
            "type_32": "左右绕行",
            "type_33": "注意信号灯",
            "type_34": "注意危险",
            "type_35": "注意行人",
            "type_36": "注意非机动车",
            "type_37": "注意儿童",
            "type_38": "向右急转弯",
            "type_39": "向左急转弯",
            "type_40": "下陡坡",
            "type_41": "上陡坡",
            "type_42": "慢行",
            "type_43": "T形交叉",
            "type_44": "T形交叉",
            "type_45": "村庄",
            "type_46": "反向弯路",
            "type_47": "无人看守铁路道口",
            "type_48": "施工",
            "type_49": "连续弯路",
            "type_50": "有人看守铁路道口",
            "type_51": "事故易发路段",
            "type_52": "停车让行",
            "type_53": "静止驶入",
            "type_54": "静止车辆临时或长时停放",
            "type_55": "静止通行",
            "type_56": "减速让行",
            "type_57": "停车检查",
        }

        #界面配置
        self.setupUi(self)
        self.setAcceptDrops(True)
        # self.imageLabel.setMinimumWidth(500)
        # self.current_label.setFrameShape(QtWidgets.QFrame.Box)
        self.current_label.setAlignment(Qt.AlignCenter)
        self.scene = QGraphicsScene(self)
        self.imageView.setScene(self.scene)
        # 当前展示的图片
        self.current_page = 0
        # 图片路径
        self.img_paths = image_paths
        # 识别结果
        self.answers = ['' for i in range(len(image_paths))]
        # 表格数据模型
        self.table_model = ''
        # 设置表格
        self.set_table()
        # 设置展示图片
        self.load_image()
        # 点击表格某一行切换图片
        # self.imageTable.cellClicked.connect(self.show_image)
        # self.imageTable..selectionChanged.connect(self.show_image)
        # self.imageTable.doubleClicked.connect(self.show_image)
        self.imageTable.clicked.connect(self.show_image)
        # 禁止编辑
        self.imageTable.setEditTriggers(QTableView.NoEditTriggers)

        # 默认模型
        self.model = self.yoloModel
        self.modelList = ["yolov8", "alexnet", "MobileVit"]
        for model in self.modelList:
            self.ModelcomboBox.addItem(model)
        self.ModelcomboBox.setCurrentIndex(0)
        # 模型修改
        self.ModelcomboBox.currentIndexChanged.connect(self.on_model_change)

        self.allButton.clicked.connect(self.recognitionAll)
        self.oneButton.clicked.connect(self.recognitionOne)
        self.prevButton.clicked.connect(self.prev_image)
        self.nextButton.clicked.connect(self.next_image)


    def change(self, image_paths):
        # 当前展示的图片
        self.current_page = 0
        # 图片路径
        self.img_paths = image_paths
        # 识别结果
        self.answers = ['' for i in range(len(image_paths))]
        # 设置表格
        self.set_table()
        # 设置展示图片
        self.load_image()

    # 更新表格
    def set_table(self):
        # 创建表格数据模型
        self.table_model = QStandardItemModel(len(self.img_paths), 1)
        # 创建表头
        self.table_model.setHorizontalHeaderLabels(['标志类别'])
        for i in range(len(self.answers)):
            # print(i)
            # self.table_model.setItem(i, 0, QStandardItem(i))
            self.table_model.setItem(i, 0, QStandardItem(self.answers[i]))

        self.imageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imageTable.setModel(self.table_model)

    # 设置模型
    def on_model_change(self, index):
        if index == 0:
            self.model = self.yoloModel
        elif index == 1:
            self.model = self.alexNet
        elif index == 2:
            self.model = self.mobileVit
            print("mobilevit")
        else:
            self.model = self.yoloModel
        print("model change to ", self.modelList[index])

    # 设置图片(并修改当前是第几张的提示)
    def load_image(self):

        pixmap = QPixmap(self.img_paths[self.current_page])
        self.scene.clear()
        # self.imageView.fitInView(self.scene.addPixmap(pixmap), Qt.KeepAspectRatio)
        self.scene.addPixmap(pixmap)
        # self.imageView.fitInView()
        # self.imageView.setScaledContents(True)
        #
        # self.imageLabel.setPixmap(pixmap)
        # self.imageLabel.setScaledContents(True)
        self.current_label.setText('第{}张'.format(self.current_page + 1))

    # 点击表格展示图片
    def show_image(self, item):
        self.current_page = item.row()
        self.load_image()

    # 切换到上一张
    def prev_image(self):
        if self.current_page == 0:
            return
        else:
            self.current_page = self.current_page - 1
            self.load_image()

    # 切换到下一张
    def next_image(self):
        if self.current_page == len(self.img_paths) - 1:
            return
        else:
            self.current_page = self.current_page + 1
            self.load_image()

    # 识别图片
    def recognitionOne(self):
        self.answers[self.current_page] = self.nameMap[self.model.recognition(self.img_paths[self.current_page])]
        print("image {} is: ".format(self.current_page), self.answers[self.current_page])
        self.set_table()

    # 识别所有图片
    def recognitionAll(self):
        for i in range(len(self.img_paths)):
            self.answers[i] = self.nameMap[self.model.recognition(self.img_paths[i])]
            print("image {} is: ".format(i), self.answers[i])
        self.set_table()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget()
        path = r"E:\TranfficSign\TrafficSign_window\Model\classification_model\testImages"
        self.detectTab = detectionTab([os.path.join(path, image) for image in os.listdir(path) if os.path.isdir(os.path.join(path))])
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