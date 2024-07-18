import os
import shutil

# 指定要遍历的目录
source_directory = 'path/to/source/directory'
# 指定目标目录，用于存放找到的图片文件
destination_directory = 'path/to/destination/directory'

# 确保目标目录存在，如果不存在则创建
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# 图片文件扩展名列表
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

# 递归遍历目录的函数
def move_images(src, dst):
    # 遍历当前目录中的所有文件和文件夹
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        # 如果是文件夹，则递归调用
        if os.path.isdir(item_path):
            move_images(item_path, dst)
        # 如果是图片文件，则移动到目标目录
        elif os.path.isfile(item_path) and any(item.lower().endswith(ext) for ext in image_extensions):
            # 构建目标文件路径
            target_path = os.path.join(dst, item)
            # 检查目标路径是否存在同名文件
            base, extension = os.path.splitext(item)
            counter = 1
            while os.path.exists(target_path):
                # 如果存在，添加后缀并重新检查
                target_path = os.path.join(dst, f"{base}_{counter}{extension}")
                counter += 1
            # 移动文件到新的目标路径
            shutil.move(item_path, target_path)

# 开始递归遍历并移动图片文件
move_images(source_directory, destination_directory)
