import onnxruntime
import onnxruntime as ort
from PIL import Image
from torchvision import transforms
import time
import os


print(onnxruntime.get_device())
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def get_img_numpy(img_path):
    image = Image.open(img_path).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0)
    input_numpy = input_tensor.numpy()
    input_data = {'images': input_numpy}
    return input_data



if __name__ == '__main__':

    myyolo = ort.InferenceSession("E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\myyolo.onnx", providers=['CUDAExecutionProvider'])
    print(myyolo.get_providers())
    yolo8 = ort.InferenceSession("E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\yolo8.onnx", providers=['CUDAExecutionProvider'])
    print(yolo8.get_providers())

    testimg = "E:\TranfficSign\ObjectCheck\\tt100k_2021\\test\\0000001.jpg"
    input_data = get_img_numpy(testimg)

    out_myyolo = myyolo.run(None, input_data)
    out_yolo8 = yolo8.run(None, input_data)

    sumtime_m = 0
    sumtime = 0
    for i in range(100):
        imglabe = "000000" + str(i)
        if len(imglabe) > 7:
            imglabe = imglabe[-7:]
        print(imglabe,end=",")
        testimg = "E:\TranfficSign\ObjectCheck\\tt100k_2021\\test\\" + imglabe + ".jpg"
        input_data = get_img_numpy(testimg)

        start_m = time.time()
        out_myyolo = myyolo.run(None, input_data)
        end_m = time.time()
        sumtime_m+=end_m - start_m
        print(end_m - start_m,end=",")

        start = time.time()
        out_yolo8 = yolo8.run(None, input_data)
        end = time.time()
        sumtime+=end - start
        print(end-start)

    print(sumtime_m,sumtime,sumtime_m/sumtime)

    # start = time.time()
    # out_yolo8 = yolo8.run(None, input_data)
    # end = time.time()
    # print(end-start)


    # fasterrcnn = ort.InferenceSession("E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\Fasterrcnnmodel.onnx")

    #
    # transform_faster = transforms.Compose([
    #     transforms.ToTensor(),
    #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    # ])
    #
    # input_tensor_f = transform_faster(image)
    # input_tensor_f = input_tensor_f.unsqueeze(0)
    # input_numpy_f = input_tensor_f.numpy()
    #
    # input_faster = {'input' : input_numpy_f}
    #
    #
    # out_fasterrcnn = fasterrcnn.run(None, input_faster)
    #
    # print(out_fasterrcnn)

