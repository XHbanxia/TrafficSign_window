import os
import sys
# import time
import threading
import queue
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsScene, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

from enhancement import Ui_imgEnhancement
from Model.ImageEnhancement.fog import fog_normal_PIL
from Model.ImageEnhancement.lowlight.SCI import lowlight_sci
from Model.ImageEnhancement.lowlight import lowlight_normal_PIL
from Model.ImageEnhancement.noise import noise_normal_median
from Model.ImageEnhancement.noise import noise_normal_gaussian
from Model.ImageEnhancement.sharpen.RealESRGAN import sharpen_realesrgan
from Model.ImageEnhancement.sharpen.SRGAN import sharpen_srgan
from Model.ImageEnhancement.sharpen import sharpen_normal_PIL

enhance_method = ["fog", "lowlight", "noise", "sharpen", "pipeline"]
model_list = [["normal_PIL"],
              ["normal_PIL", "sci"],
              ["normal_median", "normal_gaussian"],
              ["normal_PIL", "srgan", "realesrgan"],
              ["default"]]
model = [[fog_normal_PIL],
         [lowlight_normal_PIL, lowlight_sci],
         [noise_normal_median, noise_normal_gaussian],
         [sharpen_normal_PIL, sharpen_srgan, sharpen_realesrgan],
         ["default"]]


def worker(method_index, model_index, input_queue, output_queue):
    while True:
        # 从输入队列获取任务
        task = input_queue.get()
        if task is None:
            # 如果接收到 None，表示任务结束，退出循环
            break
        # 调用 sharpen_normal 包中的函数，处理任务
        result = model[method_index][model_index].inference(task)
        # 将处理结果放入输出队列
        output_queue.put(result)


class enhance(QWidget, Ui_imgEnhancement):
    def __init__(self,callback=None):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.callback = callback

        # 模型与输入输出
        self.imgPath = None
        self.result = None

        # 选择处理方式
        self.enhance_method.addItems(enhance_method)
        self.enhance_method.currentIndexChanged.connect(self.method_change)
        # 选择具体模型
        self.selected_model.addItems(model_list[self.enhance_method.currentIndex()])
        self.selected_model.currentIndexChanged.connect(self.model_change)

        # 模型
        self.model = model[self.enhance_method.currentIndex()][self.selected_model.currentIndex()]
        # 预测
        self.enhance_pushButton.clicked.connect(self.predict)

        # 展示输入输出
        self.scene_origin = QGraphicsScene(self)  # 原图画布
        self.pixmapItem_origin = None
        self.graphicsView.setScene(self.scene_origin)
        self.scene_result = QGraphicsScene(self)  # 输出图画布
        self.pix = None
        self.pixmapItem_result = None
        self.graphicsView_2.setScene(self.scene_result)

        # 保存结果
        save_path = '/Model/ImageEnhancement/data/GuiResult/result.jpg'
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        parent_last_dir = os.path.dirname(script_dir)
        parent_dir = os.path.dirname(parent_last_dir)
        self.savePath = parent_dir+save_path
        # print(self.savePath)
        self.save_button.clicked.connect(self.save)

    def img_change(self):
        pixmap = QPixmap(self.imgPath)
        if self.scene_origin is not None:
            self.scene_origin.clear()
        self.pixmapItem_origin = self.scene_origin.addPixmap(pixmap)
        self.graphicsView.fitInView(self.pixmapItem_origin, Qt.KeepAspectRatio)

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
            self.imgPath = event.mimeData().urls()[0].toLocalFile()
            # if self.callback:
            #     self.callback(self.imgpath)
            #     print("callback...")
            # print(self.imgpath)
            self.img_change()
            print("已切换待处理图片")
        else:
            event.ignore()
            print("ignored")

    def method_change(self, index):
        # print(index)
        self.selected_model.clear()
        for mo in model_list[index]:
            self.selected_model.addItem(mo)
        print("method change to ", enhance_method[index])

    def model_change(self, index):
        temp_index = self.enhance_method.currentIndex()
        self.model = model[temp_index][index]
        print("model change to ", model_list[temp_index][index])

    def predict(self):
        print("开始增强")
        # 创建输入队列和输出队列
        input_queue = queue.Queue()
        output_queue = queue.Queue()
        # 创建子进程
        # worker_time = time.perf_counter()
        thread = threading.Thread(target=worker,
                                  args=(self.enhance_method.currentIndex(),
                                        self.selected_model.currentIndex(),
                                        input_queue, output_queue))
        thread.start()
        # 发送任务给子进程
        tasks = [self.imgPath]  # 你的任务列表
        for task in tasks:
            input_queue.put(task)
        # 从输出队列获取处理结果，并将结果赋值
        for _ in range(len(tasks)):
            self.result = output_queue.get()
        # 发送 None 表示任务结束
        input_queue.put(None)
        # 等待子进程结束
        thread.join()


        q_image = QImage(self.result.tobytes(), self.result.width, self.result.height, QImage.Format_RGB888)
        self.scene_result.clear()  # 清空残留
        self.pix = QPixmap.fromImage(q_image)
        self.pixmapItem_result = self.scene_result.addPixmap(self.pix)

        self.graphicsView_2.fitInView(self.pixmapItem_result, Qt.KeepAspectRatio)
        print("增强完成")

    def save(self):
        self.result.save(self.savePath, 'JPEG')
        if self.callback:
            self.callback(self.savePath)
            print("callback...")
        print("图片已保存至", self.savePath)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.detectTab = enhance()
        self.tab1 = QTabWidget()
        self.tab_widget.addTab(self.detectTab, "enhancement")
        self.setCentralWidget(self.tab_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyWindow()
    # tab = detectionTab()
    # MainWindow.setCentralWidget(tab)
    MainWindow.show()
    sys.exit(app.exec_())
