# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 9:00
# @Author  : 10148
import time
from ultralytics import YOLO
import cv2


class Track:
    def __init__(self, model, vid_path, window_name):
        super().__init__()
        self.model = model
        self.vid_path = vid_path
        self.window_name = window_name
        self.start_time = time.time()
        self.frames_processed = 0
        self.fps = 0  # 添加 fps 属性

    def run(self):
        self.model = YOLO(self.model)
        result = self.model.track(self.vid_path, verbose=True, stream=True)
        cv2.namedWindow(self.window_name, cv2.WINDOW_FREERATIO)
        for res in result:
            ann = res.plot()
            # Calculate FPS
            self.cal_fps()
            # Put the FPS text on the frame top-left corner
            cv2.putText(ann, f"FPS: {round(self.fps, 2)}", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                        2)
            cv2.imshow(self.window_name, ann)

            # 检查是否需要停止
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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
    model = '../weights/OpenPit.pt'
    vid = "../data/DJI_0002_1080.mp4"
    window_name = 'track'
    truck = Track(model, vid, window_name)
    truck.run()


if __name__ == '__main__':
    main()
