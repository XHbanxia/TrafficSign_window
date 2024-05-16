import os
from ultralytics import YOLO
import logging
# from io import StringIO
from Model.detect_model.logger import get_log_time
# log_capture_string = StringIO()

# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)
weights_path = os.path.join(parent_dir, 'modelWeights', 'myyolo.pt')
modul = YOLO(weights_path)
# success = modul.export(format="onnx",opset=12)

# logger = logging.getLogger('ultralytics')
# stream_handler = logging.StreamHandler(log_capture_string)
# stream_handler.setLevel(logging.INFO)
# logger.addHandler(stream_handler)




def prodectfunc(img_path):
    print("prodect by my youlo")
    print(img_path)

    results = modul.predict(source=img_path)
    log_contents = get_log_time()
    print(log_contents)

    return results[0].boxes.xywh,log_contents

# def modulesummary():
#     summary(your_model, input_size=(channels, height, width))



if __name__ == '__main__':

    # file_path = r"E:\TranfficSign\TrafficSign_window\Model\detect_model\time.txt"
    # with open(file_path, "w") as file:
    #     file.write("Myyolo runtime \n")

    # summarymodul = torch.load("E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\myyolo.pt")
    # summary(summarymodul, input_size=(3, 2048, 2048))

    for i in range(10):
        imglabe = "000000"+str(i)
        if len(imglabe)>7:
            imglabe = imglabe[-7:]
        print(imglabe)
        testimg = "E:\TranfficSign\ObjectCheck\\tt100k_2021\\test\\" + "2" + ".jpg"
        results = prodectfunc(testimg)
    # print(results)