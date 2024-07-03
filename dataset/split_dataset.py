import os
import shutil
import random

f_train = open('train.txt', 'w')
f_valid = open('valid.txt', 'w')

path1 = r'D:/B_Dataset/infrared/images'
path2 = r'D:/B_Dataset/infrared/labels'
outpath_train_jpg = 'D:/B_Dataset/infrared/images/train'
outpath_train_txt = 'D:/B_Dataset/infrared/labels/train'
outpath_valid_jpg = 'D:/B_Dataset/infrared/images/val'
outpath_valid_txt = 'D:/B_Dataset/infrared/labels/val'

if not os.path.exists(outpath_train_jpg):
    os.makedirs(outpath_train_jpg)
if not os.path.exists(outpath_train_txt):
    os.makedirs(outpath_train_txt)
if not os.path.exists(outpath_valid_jpg):
    os.makedirs(outpath_valid_jpg)
if not os.path.exists(outpath_valid_txt):
    os.makedirs(outpath_valid_txt)

train_jpg_list = []
train_text_list = []
valid_jpg_list = []
valid_text_list = []

# 随机选取20%的数据作为验证集 剩下80%作为训练集
file_list_jpg = []
file_list_txt = []
for image in os.listdir(path1):
    if 'jpg' in image:
        temp = os.path.join(path1, image).replace('\\', '/')
        file_list_jpg.append(temp)

random.shuffle(file_list_jpg)
total_files = len(file_list_jpg)
train_ratio = 0.8
train_files = file_list_jpg[:int(total_files * train_ratio)]
valid_files = file_list_jpg[int(total_files * train_ratio):]
# 把文件移动到对应的文件夹中

for file_path in train_files:
    shutil.move(file_path, outpath_train_jpg)
    train_jpg_list.append(os.path.join(outpath_train_jpg, file_path.split('/')[-1]))
    # 获取文件名并替换扩展名
    filename = file_path.split('/')[-1]
    label_name = filename.replace('jpg', 'txt')
    # 构建正确的标签文件路径
    label_path = os.path.join(path2, label_name)
    # 打印标签文件的路径，以便调试
    print(f"Label file path: {label_path}")
    # 检查标签文件是否存在
    if os.path.exists(label_path):
        shutil.move(label_path, outpath_train_txt)
        train_text_list.append(os.path.join(outpath_train_txt, label_name))
    else:
        print(f"Label file not found for {file_path}")


for file_path in valid_files:
    shutil.move(file_path, outpath_valid_jpg)
    valid_jpg_list.append(os.path.join(outpath_valid_jpg, file_path.split('/')[-1]))
    # 获取文件名并替换扩展名
    filename = file_path.split('/')[-1]
    label_name = filename.replace('jpg', 'txt')
    # 构建正确的标签文件路径
    label_path = os.path.join(path2, label_name)
    # 检查标签文件是否存在
    if os.path.exists(label_path):
        shutil.move(label_path, outpath_valid_txt)
        valid_text_list.append(os.path.join(outpath_valid_txt, label_name))
    else:
        print(f"Label file not found for {file_path}")


# 写入txt文件
for file_path in train_jpg_list:
    f_train.write(file_path + '\n')
print("Train set created.")
print("Number of train samples:", len(train_jpg_list))

for file_path in valid_jpg_list:
    f_valid.write(file_path + '\n')
print("Validation set created.")
print("Number of validation samples:", len(valid_jpg_list))
