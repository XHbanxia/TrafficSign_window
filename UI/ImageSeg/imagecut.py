import os
import shutil

from PIL import Image
from Model.detect_model.my_yolo import myyolo

script_path = os.path.abspath(__file__)
script_dir_1 = os.path.dirname(script_path)
script_dir_2 = os.path.dirname(script_dir_1)
script_dir = os.path.dirname(script_dir_2)
imgPath = os.path.join(script_dir,"Model","seg_model","data")
# save_path = os.path.join(script_dir,"result_k_means")
print(imgPath)

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

def delete_file(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def save_cutImg(img_path,xywh):
    # 这里我调了我的yolo来做测试，主要是生成那个框框的数据
    # xywh = myyolo.prodectfunc(img_path)
    for item in xywh:
        print(item)
    crop_image = cutimge(img_path, xywh)
    i = 0
    # imgPath = r"D:\PyCharm\PyCharm Community Edition 2021.2\PycharmProjects\pyqt_ui\TrafficSign_window-master\Model\seg_model\data"
    delete_file(imgPath)

    for item in crop_image:
        imgPath0 = imgPath + "/" + str(i) + ".png"
        i = i + 1
        item.save(imgPath0, "PNG")
    return imgPath0

# if __name__=="__main__":
#     img_path = r"D:\PyCharm\PyCharm Community Edition 2021.2\PycharmProjects\pyqt_ui\TrafficSign_window-master\Model\detect_model\0000002.jpeg"
