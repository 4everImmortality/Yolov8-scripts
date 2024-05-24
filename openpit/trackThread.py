# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 14:15
# @Author  : 10148

import time
from ultralytics import YOLO
import cv2
import threading
from queue import Queue


class DetectionThread(threading.Thread):
    def __init__(self, model, vid_path, output_queue, completion_flag):
        super().__init__()
        self.model = YOLO(model)
        self.vid_path = vid_path
        self.output_queue = output_queue
        self.completion_flag = completion_flag
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        result = self.model.track(self.vid_path, verbose=True, stream=True)
        for res in result:
            self.output_queue.put(res)
            if self._stop_event.is_set():
                break

        # Set the completion flag when the video stream ends
        self.completion_flag.set()


def main():
    model = '../weights/OpenPit.pt'
    vid = "../data/DJI_0002_1080.mp4"
    window_name = 'track'

    output_queue = Queue()
    completion_flag = threading.Event()

    detection_thread = DetectionThread(model, vid, output_queue, completion_flag)
    detection_thread.start()

    cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)

    start_time = time.time()
    frames_processed = 0
    fps = 0

    try:
        while True:
            if not output_queue.empty():
                ann = output_queue.get()
                ann = ann.plot()

                current_time = time.time()
                elapsed_time = current_time - start_time
                frames_processed += 1

                if elapsed_time > 0.1:  # 计算每秒的帧率
                    fps = frames_processed / elapsed_time
                    start_time = current_time
                    frames_processed = 0

                cv2.putText(ann, f"FPS: {round(fps, 2)}", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.imshow(window_name, ann)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    detection_thread.stop()
                    break

            time.sleep(0.01)  # 避免线程间过于频繁的通信

            # Check if the completion flag is set to exit when the video stream ends
            if completion_flag.is_set():
                break

    except KeyboardInterrupt:
        detection_thread.stop()
        detection_thread.join()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
