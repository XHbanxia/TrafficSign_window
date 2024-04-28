import os

from ultralytics import YOLO

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)
weights_path = os.path.join(parent_dir, 'modelWeights', 'yolo8.pt')
modul = YOLO(weights_path)
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