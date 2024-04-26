from ultralytics import YOLO
import cv2
import numpy as np


modul=YOLO(r"E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\yolo8.pt")
def prodectfunc(img_path):
    print("prodecting by yolo8")
    print(img_path)

    results = modul.predict(source=img_path)
    # print(results[0].boxes)

    return results[0].boxes.xywh


if __name__ == '__main__':
    testimg = r"E:\TranfficSign\ObjectCheck\tt100k_2021\test\0000013.jpg"
    results = prodectfunc(testimg)
    # print(results)