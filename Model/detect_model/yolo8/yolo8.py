import os
import torch
from ultralytics import YOLO
import time
from Model.detect_model.logger import get_log_time
from PIL import Image

# import logging
# from io import StringIO
#
# log_capture_string = StringIO()


# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)
file_path = os.path.join(parent_dir, 'time.txt')
weights_path = os.path.join(parent_dir, 'modelWeights', 'yolo8-new.pt')
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
# print(torch.cuda.is_available())
modul = YOLO(weights_path)

# logger = logging.getLogger('ultralytics')
# stream_handler = logging.StreamHandler(log_capture_string)
# stream_handler.setLevel(logging.INFO)
# logger.addHandler(stream_handler)

# success = modul.export(format="onnx",opset=12)
def prodectfunc(img_path):
    print("prodecting by yolo8")
    # torch.cuda.empty_cache()

    results = modul.predict(source=img_path)

    log_contents = get_log_time()
    print(log_contents)


    return results[0].boxes.xywh,log_contents


if __name__ == '__main__':

    # file_path = r"E:\TranfficSign\TrafficSign_window\Model\detect_model\time.txt"
    # with open(file_path, "w") as file:
    #     file.write("Yolo runtime \n")

    for i in range(2):
        imglabe = "000000" + str(i)
        if len(imglabe) > 7:
            imglabe = imglabe[-7:]
        print(imglabe)
        testimg = "E:\TranfficSign\ObjectCheck\\tt100k_2021\\test\\" + imglabe + ".jpg"
        results = prodectfunc(testimg)
    # print(results)