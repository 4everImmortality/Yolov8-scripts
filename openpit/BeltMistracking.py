# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 15:53
# @Author  : 10148

from ultralytics import YOLO
import cv2
import time
from threading import Thread
import queue

'''
    皮带机跑偏检测，使用YOLOv8
    设置2个线程，一个用于检测，一个用于显示
    实时目标检测，检测到皮带机跑偏后，在图像上显示跑偏，用来预警
    检测线程和显示线程都是死循环，直到按下q键退出
    检测线程检测到皮带机跑偏后，会将跑偏的方向输出到控制台
    检测不到轮子就意味着跑偏了
    检测到轮子就意味着没有跑偏
    进程间通信使用队列，检测线程将检测结果放入队列，显示线程从队列中取出检测结果
'''


# 检测线程
class DetectThread(Thread):
    def __init__(self, model, vid_path, render_queue, window_name):
        super().__init__()
        self.model = model
        self.vid_path = vid_path
        self.render_queue = render_queue
        self.window_name = window_name
        self._stop_event = False
        self.start_time = time.time()
        self.frames_processed = 0
        self.fps = 0  # 添加 fps 属性

    def stop(self):
        self._stop_event = True

    def run(self):
        results = self.model.predict(self.vid_path, stream=True, verbose=False)
        for result in results:
            if self._stop_event is True:
                break
            ann = result.plot()
            # Calculate FPS
            self.cal_fps()
            # Put the FPS text on the frame top-left corner
            cv2.putText(ann, f"FPS: {round(self.fps, 2)}", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            self.render_queue.put((ann, result.tojson()))
        self.stop()

    def cal_fps(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        self.frames_processed += 1

        # 计算实际的帧率
        if elapsed_time > 0.1:  # 这里设置一个时间阈值，例如0.1秒
            self.fps = self.frames_processed / elapsed_time
            self.start_time = current_time
            self.frames_processed = 0


# 在主线程中显示图片

def main():
    model_path = '../weights/Belt.pt'
    vid = '../data/Belt.mp4'
    model = YOLO(model_path)
    render_queue = queue.Queue()
    window_name = 'Belt'
    detect_thread = DetectThread(model, vid, render_queue, window_name)
    detect_thread.start()
    cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)
    while True:
        # 显示检测结果
        if not render_queue.empty():
            img = render_queue.get()[0]
            json_data = render_queue.get()[1]
            # 统计轮子数量 字符串中 "class": 3 的数量
            wheel_count = json_data.count('"class": 3')
            if wheel_count < 6:
                cv2.putText(img, f"Warning: Belt Mistracking!", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif wheel_count == 6:
                cv2.putText(img, f"Belt is normal!", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if json_data.count('"class": 0') > 0:
                cv2.putText(img, f"Belt is stop!", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
            cv2.imshow(window_name, img)
        # 按下q键退出
        if cv2.waitKey(1) == ord('q') or detect_thread._stop_event is True:
            cv2.destroyAllWindows()
            detect_thread.stop()
            break
    cv2.destroyAllWindows()
    detect_thread.join()


if __name__ == '__main__':
    main()
