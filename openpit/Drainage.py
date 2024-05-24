# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 15:54
# @Author  : 10148

from ultralytics import YOLO
import cv2
import time
from threading import Thread
import queue
import warnings

warnings.filterwarnings('ignore')

'''
    探放水检测，使用YOLOv8
    设置2个线程，一个用于检测，一个用于显示
    检测线程检测到的结果放入队列，显示线程从队列中取出结果并显示
    探放水一次的流程：检测结果中有drill 就增加计数，显示在屏幕上
    按下s键清空计数，按下q键退出程序
'''


# 检测线程
class DetectThread(Thread):
    def __init__(self, model_path, vid_path, render_queue, window_name):
        super().__init__()
        self.model = YOLO(model_path)
        self.vid_path = vid_path
        self.render_queue = render_queue
        self.window_name = window_name
        self._stop_event = False
        self.start_time = time.time()
        self.frames_processed = 0
        self.fps = 0

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
            cv2.putText(ann, f"FPS: {round(self.fps, 2)}", (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
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


def main():
    model_path = '../weights/Drainage.pt'
    vid = '../data/Drainage.mp4'
    render_queue = queue.Queue()
    window_name = 'Drainage'

    detect_thread = DetectThread(model_path, vid, render_queue, window_name)
    detect_thread.start()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    count = 0
    flag = True

    try:
        while True:
            if not render_queue.empty():
                img, json_data = render_queue.get()

                if json_data.count('"class": 3') > 0 and flag:
                    count += 1
                    flag = False
                elif json_data.count('"class": 3') == 0:
                    flag = True

                cv2.putText(img, f"Drainage Count {count}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow(window_name, img)

            key = cv2.waitKey(1)

            if key == ord('q') or detect_thread._stop_event:
                break

            elif key == ord('s'):
                count = 0

    except Exception as e:
        print(f"Exception: {e}")

    finally:
        cv2.destroyAllWindows()
        detect_thread.stop()
        detect_thread.join()


if __name__ == '__main__':
    main()
