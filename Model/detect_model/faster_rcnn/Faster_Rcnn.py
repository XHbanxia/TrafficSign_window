import os
import time

import torch
from thop import profile

from PIL import Image

from torchvision import transforms
from Model.detect_model.faster_rcnn.network_files import FasterRCNN
from Model.detect_model.faster_rcnn.backbone import resnet50_fpn_backbone
from torchsummary import summary

def create_model(num_classes):
    # mobileNetv2+faster_RCNN
    # backbone = MobileNetV2().features
    # backbone.out_channels = 1280
    #
    # anchor_generator = AnchorsGenerator(sizes=((32, 64, 128, 256, 512),),
    #                                     aspect_ratios=((0.5, 1.0, 2.0),))
    #
    # roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0'],
    #                                                 output_size=[7, 7],
    #                                                 sampling_ratio=2)
    #
    # model = FasterRCNN(backbone=backbone,
    #                    num_classes=num_classes,
    #                    rpn_anchor_generator=anchor_generator,
    #                    box_roi_pool=roi_pooler)

    # resNet50+fpn+faster_RCNN
    # 注意，这里的norm_layer要和训练脚本中保持一致
    backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d)
    model = FasterRCNN(backbone=backbone, num_classes=num_classes, rpn_score_thresh=0.5)

    return model


def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()


def prodectfunc(img):


    # get devices
    print("preditcing by FasterRcnn")


    # load image
    original_img = Image.open(img)

    # from pil image to tensor, do not normalize image
    data_transform = transforms.Compose([transforms.ToTensor()])
    img = data_transform(original_img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    with torch.no_grad():
        # init
        img_height, img_width = img.shape[-2:]
        init_img = torch.zeros((1, 3, img_height, img_width), device=device)
        model(init_img)

        t_start = time_synchronized()
        predictions = model(img.to(device))[0]
        t_end = time_synchronized()
        # print("inference+NMS time: {}".format(t_end - t_start))

        predict_boxes = predictions["boxes"].tolist()
        predict_classes = predictions["labels"].tolist()
        predict_scores = predictions["scores"].tolist()

        if len(predict_boxes) == 0:
            print("没有检测到任何目标!")

        result = []

        for item in range(len(predict_classes)):
            if predict_scores[item]>0.6:
                cx = (predict_boxes[item][0]+predict_boxes[item][2])/2
                cy = (predict_boxes[item][1]+predict_boxes[item][3])/2
                w = predict_boxes[item][3]-predict_boxes[item][1]
                h = predict_boxes[item][2]-predict_boxes[item][0]
                predict_boxes[item][0] = cx
                predict_boxes[item][1] = cy
                predict_boxes[item][2] = w
                predict_boxes[item][3] = h
                result.append(predict_boxes[item])

        returntime = round((t_end - t_start)*1000, 1)

        # original_img = Image.open(r"E:\TranfficSign\ObjectCheck\tt100k_2021\test\0000002.jpg")
        # data_transform = transforms.Compose([transforms.ToTensor()])
        # img = data_transform(original_img)
        # # expand batch dimension
        # img = torch.unsqueeze(img, dim=0)

        return result,returntime

def model_complexity_info(model, input_size, device):
    input = torch.randn(input_size).to(device)
    flops, params = profile(model, inputs=(input, ))
    print('FLOPs: {}'.format(flops))
    print('Params: {}'.format(params))


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)
# label_json_path = os.path.join(script_dir, 'pascal_voc_classes.json')
weights_path = os.path.join(parent_dir, 'modelWeights', 'resNetFpn-model-3.pth')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print("using {} device.".format(device))

# create model
model = create_model(num_classes=4)

# load train weights
assert os.path.exists(weights_path), "{} file dose not exist.".format(weights_path)
weights_dict = torch.load(weights_path, map_location='cpu')
weights_dict = weights_dict["model"] if "model" in weights_dict else weights_dict
model.load_state_dict(weights_dict)
model.to(device)
# model_complexity_info(model,(1,3,2048,2048),device)
# torch.save(model,"E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\Fastercnn.pth")
model.eval()  # 进入验证模式

# model = model.cuda()
# input_data = input_data.cpu()
# summary(model,input_size=(3,2048,2048))



# x = torch.randn(1, 3, 2048, 2048)
# x = x.cuda()
#
# # 设置导出的ONNX文件名
# onnx_file_name = "Fasterrcnnmodel.onnx"
#
# # 导出模型
# torch.onnx.export(model,               # 模型
#                   x,                   # 输入张量
#                   onnx_file_name,      # ONNX文件名
#                   export_params=True,  # 导出模型中的参数
#                   opset_version=12,    # ONNX版本
#                   do_constant_folding=True,  # 是否执行常量折叠优化
#                   input_names=['input'],     # 输入名
#                   output_names=['output'],   # 输出名
#                   dynamic_axes={'input': {0: 'batch_size'},  # 批处理变量
#                                 'output': {0: 'batch_size'}})



if __name__ == '__main__':

    sumtime = 0
    for i in range(1):
        imglabe = "000000" + str(i)
        if len(imglabe) > 7:
            imglabe = imglabe[-7:]
        # print(imglabe,end=",")
        testimg = "E:\TranfficSign\ObjectCheck\\tt100k_2021\\test\\" + imglabe + ".jpg"
        result,runtime = prodectfunc(testimg)
        sumtime+=runtime
        print(runtime)
    print(sumtime)