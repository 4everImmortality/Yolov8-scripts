import os

# 指定文件夹路径
folder_path = r'D:\B_Dataset\infrared-4\labels\train'
# 指定数字列表
numbers_list = [0, 1, 4, 5, 8]  # 示例数字列表

# 存储处理后的文件内容
processed_contents = []

# 遍历文件夹内的所有txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 存储处理后的文件内容
        processed_lines = []
        for line in lines:
            try:
                # 尝试解析行首的数字
                first_number = int(line.split()[0])
                # 如果数字不在列表中，则保留该行
                if first_number not in numbers_list:
                    processed_lines.append(line)
            except (ValueError, IndexError):
                # 如果解析失败（例如行首不是数字），则保留该行
                processed_lines.append(line)

        # 将处理后的文件内容添加到数组中
        processed_contents.append(''.join(processed_lines))

# 输出处理后的内容
for content in processed_contents:
    print(content)
