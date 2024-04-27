from PIL import Image
from Model.detect_model.my_yolo import myyolo

def cutimge(imagepath,xywh):
    image = Image.open(imagepath)
    cropped_images = []

    xywh = xywh.tolist()
    # 遍历列表中的每个框
    for x, y, w, h in xywh:
        # 计算裁剪框的左上角和右下角坐标
        left = x - w // 2
        top = y - h // 2
        right = x + w // 2
        bottom = y + h // 2

        # print(left, top, right, bottom)
        # 裁剪图片
        cropped_image = image.crop((left, top, right, bottom))
        cropped_images.append(cropped_image)

    # 返回裁剪后的图片列表
    return cropped_images


if __name__=="__main__":
    img_path = r"E:\TranfficSign\ObjectCheck\tt100k_2021\test\0000002.jpg"
    # 这里我调了我的yolo来做测试，主要是生成那个框框的数据
    xywh = myyolo.prodectfunc(img_path)
    # for item in xywh:
    #     print(item)
    crop_image = cutimge(img_path, xywh)
    # 展示图片
    for item in crop_image:
        item.show()