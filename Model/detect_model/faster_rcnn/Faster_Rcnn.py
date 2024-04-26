import os
import time
import json

import torch
import torchvision
from PIL import Image
import matplotlib.pyplot as plt

from torchvision import transforms
from Model.detect_model.faster_rcnn.network_files import FasterRCNN
from Model.detect_model.faster_rcnn.backbone import resnet50_fpn_backbone, MobileNetV2


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
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # print("using {} device.".format(device))

    # create model
    model = create_model(num_classes=4)

    # load train weights
    weights_path = r"E:\TranfficSign\TrafficSign_window\Model\detect_model\modelWeights\resNetFpn-model-3.pth"
    assert os.path.exists(weights_path), "{} file dose not exist.".format(weights_path)
    weights_dict = torch.load(weights_path, map_location='cpu')
    weights_dict = weights_dict["model"] if "model" in weights_dict else weights_dict
    model.load_state_dict(weights_dict)
    model.to(device)

    # read class_indict
    label_json_path = r"E:\TranfficSign\TrafficSign_window\Model\detect_model\faster_rcnn\pascal_voc_classes.json"
    assert os.path.exists(label_json_path), "json file {} dose not exist.".format(label_json_path)
    with open(label_json_path, 'r') as f:
        class_dict = json.load(f)

    category_index = {str(v): str(k) for k, v in class_dict.items()}

    # load image
    original_img = Image.open(img)

    # from pil image to tensor, do not normalize image
    data_transform = transforms.Compose([transforms.ToTensor()])
    img = data_transform(original_img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    model.eval()  # 进入验证模式
    with torch.no_grad():
        # init
        img_height, img_width = img.shape[-2:]
        init_img = torch.zeros((1, 3, img_height, img_width), device=device)
        model(init_img)

        t_start = time_synchronized()
        predictions = model(img.to(device))[0]
        t_end = time_synchronized()
        print("inference+NMS time: {}".format(t_end - t_start))

        predict_boxes = predictions["boxes"].tolist()
        predict_classes = predictions["labels"].tolist()
        predict_scores = predictions["scores"].tolist()

        if len(predict_boxes) == 0:
            print("没有检测到任何目标!")

        result = []

        for item in range(len(predict_classes)):
            if predict_scores[item]>0.6:
                w = predict_boxes[item][3]-predict_boxes[item][1]
                h = predict_boxes[item][2]-predict_boxes[item][0]
                predict_boxes[item][2] = w
                predict_boxes[item][3] = h
                result.append(predict_boxes[item])


        return result



if __name__ == '__main__':
    testimg = r"E:\TranfficSign\ObjectCheck\tt100k_2021\test\0000013.jpg"
    result = prodectfunc(testimg)
    print(result)