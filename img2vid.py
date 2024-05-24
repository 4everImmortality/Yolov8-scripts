# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/19 10:38
# @Author  : 10148

import cv2
import os

size = (1280, 720)

# 完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
videowrite = cv2.VideoWriter(r"out.mp4", -1, 25, size)  # 25是帧数，size是图片尺寸
img_array = []

path = r"D:\DataSet\dongbo-000001-000001-R01C0001-2023022001"  # 连续帧的文件夹路径

for fn in os.listdir(path):
    # 文件名以.jpg结尾的为图片
    if fn.endswith('.jpg'):
        filename = os.path.join(path, fn)
        img = cv2.imread(filename)
        if img is None:
            print(filename + "为空!")
            continue
        videowrite.write(img)

videowrite.release()
print('end!')
