import os
import shutil


def move_similar_files(src_folder1, src_folder2, dest_folder1, dest_folder2):
    # 确保目标文件夹存在，如果不存在则创建它们
    if not os.path.exists(dest_folder1):
        os.makedirs(dest_folder1)
    if not os.path.exists(dest_folder2):
        os.makedirs(dest_folder2)

    # 获取每个源文件夹中的所有文件名
    files1 = set(
        [os.path.splitext(f)[0] for f in os.listdir(src_folder1) if os.path.isfile(os.path.join(src_folder1, f))])
    files2 = set(
        [os.path.splitext(f)[0] for f in os.listdir(src_folder2) if os.path.isfile(os.path.join(src_folder2, f))])

    # 找到两个集合中的交集，即具有相同基本名称的文件
    common_files = files1.intersection(files2)

    # 移动文件
    for file_base_name in common_files:
        for src_folder, dest_folder in [(src_folder1, dest_folder1), (src_folder2, dest_folder2)]:
            for filename in os.listdir(src_folder):
                base, ext = os.path.splitext(filename)
                if base == file_base_name:
                    shutil.move(os.path.join(src_folder, filename), os.path.join(dest_folder, filename))
                    break  # 已经找到了并移动了文件，跳出循环


# 使用方法：
move_similar_files('D:/B_Dataset/infrared/images', 'D:/B_Dataset/infrared/labels', 'D:/B_Dataset/infrared/images1',
                   'D:/B_Dataset/infrared/labels1')
