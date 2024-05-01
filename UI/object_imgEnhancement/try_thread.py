import threading
import queue
from Model.ImageEnhancement.fog import fog_normal_PIL


def worker(input_queue, output_queue):
    while True:
        # 从输入队列获取任务
        task = input_queue.get()
        if task is None:
            # 如果接收到 None，表示任务结束，退出循环
            break
        # 调用 sharpen_normal 包中的函数，处理任务
        result = fog_normal_PIL.inference(task)
        # 将处理结果放入输出队列
        output_queue.put(result)


if __name__ == "__main__":
    # 创建输入队列和输出队列
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    # 创建子进程
    thread = threading.Thread(target=worker, args=(input_queue, output_queue))
    thread.start()

    # 在这里设置你的 img 对象
    img = None
    img_path = r"E:\勃\寒窗苦读\大四\毕业设计\TrafficSign_window\Model\ImageEnhancement\fog\fogExample.jpg"

    # 发送任务给子进程
    tasks = [img_path]  # 你的任务列表
    for task in tasks:
        input_queue.put(task)

    # 从输出队列获取处理结果，并将结果赋值给 img 对象
    for _ in range(len(tasks)):
        result = output_queue.get()
        # 假设 result 是图像数据，将其赋值给 img 对象
        img = result

    # 发送 None 表示任务结束
    input_queue.put(None)

    # 等待子进程结束
    thread.join()

    img.show()
    print("Image processing completed.")
