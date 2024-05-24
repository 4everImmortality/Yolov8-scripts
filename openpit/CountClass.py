# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 18:34
# @Author  : 10148

import os

'''
    遍历一个文件夹内的全部txt文件，读取每行的第一个数字，统计有多少个不同的数字
'''


def count_unique_classes_in_folder(folder_path):
    unique_numbers = set()
    # 遍历文件夹中的每个文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            # 打开文件
            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r') as file:
                # 读取每行的第一个数字
                for line in file.readlines():
                    number = line.split(' ')[0]
                    # 添加到集合中
                    unique_numbers.add(number)
    return len(unique_numbers), unique_numbers


if __name__ == "__main__":
    # folder_path = r"D:\DataSet\dongbo-000001-000001-R01C0001-2023022001"  # Replace with the path to your folder
    folder_path = r"D:\DataSet\hll-15217pdjt-2022072901"  # Replace with the path to your folder
    count, unique_numbers = count_unique_classes_in_folder(folder_path)

    print(f"Total unique numbers: {count}")
    print("Unique numbers:", unique_numbers)
