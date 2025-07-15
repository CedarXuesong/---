import os
import math
from PIL import Image

def split_image(image_path, m, n, output_dir):
    """
    将一张图片分割成 m x n 的图块。

    每个图块都会被保存为一个正方形的PNG图片。原始图片内容不会被拉伸。
    如果图块的区域小于正方形，剩余部分将用透明背景填充。

    Args:
        image_path (str): 输入图片的路径。
        m (int): 要将图片分割成的行数。
        n (int): 要将图片分割成的列数。
        output_dir (str): 保存输出图片的目录。
    """
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"错误：在路径 {image_path} 未找到图片文件。")
        return

    # 将图片转换为RGBA模式，以确保它有alpha通道用于透明度
    image = image.convert("RGBA")
    img_width, img_height = image.size

    # 计算网格中每个子图片的理论尺寸
    sub_img_width = img_width / n
    sub_img_height = img_height / m

    # 输出的正方形边长取子图片尺寸中较大者的向上取整
    square_size = math.ceil(max(sub_img_width, sub_img_height))

    # 计算能容纳居中图像的总画布尺寸
    total_grid_width = n * square_size
    total_grid_height = m * square_size

    # 计算图像在总画布中居中所需的偏移量
    offset_x = (total_grid_width - img_width) // 2
    offset_y = (total_grid_height - img_height) // 2

    # 如果输出目录不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出文件夹: {output_dir}")

    for i in range(m):
        for j in range(n):
            # 创建一个新的带有透明背景的正方形图片
            square_img = Image.new("RGBA", (square_size, square_size), (0, 0, 0, 0))

            # 计算当前方块在总画布中的位置
            # 并以此反推需要从原图中裁剪的区域
            source_crop_left = j * square_size - offset_x
            source_crop_top = i * square_size - offset_y
            source_crop_right = source_crop_left + square_size
            source_crop_bottom = source_crop_top + square_size

            # 确定实际裁剪区域与原图的交集
            actual_crop_left = max(0, source_crop_left)
            actual_crop_top = max(0, source_crop_top)
            actual_crop_right = min(img_width, source_crop_right)
            actual_crop_bottom = min(img_height, source_crop_bottom)
            
            # 如果交集有效，则进行裁剪和粘贴
            if actual_crop_left < actual_crop_right and actual_crop_top < actual_crop_bottom:
                # 裁剪子图片
                sub_image = image.crop((actual_crop_left, actual_crop_top, actual_crop_right, actual_crop_bottom))

                # 计算粘贴到当前方块内的位置
                paste_x = actual_crop_left - source_crop_left
                paste_y = actual_crop_top - source_crop_top
                
                square_img.paste(sub_image, (paste_x, paste_y))

            # 保存最终的正方形图片
            output_filename = os.path.join(output_dir, f"square_{i}_{j}.png")
            square_img.save(output_filename)
            print(f"已保存 {output_filename}")

    print("图片分割完成。")

if __name__ == "__main__":
    # --- 配置 ---
    # 请将 'test.png' 替换为您的图片文件名
    INPUT_IMAGE = "test.png" 
    
    # m: 您希望将图片分割成的行数
    ROWS = 3
    
    # n: 您希望将图片分割成的列数
    COLS = 4
    
    # 保存分割后图片的文件夹名称
    OUTPUT_DIR = "result"
    # ------------

    print("开始处理图片...")
    print(f"输入图片: {INPUT_IMAGE}")
    print(f"分割成: {ROWS} 行 x {COLS} 列")

    # 检查Pillow库是否安装
    try:
        from PIL import Image
    except ImportError:
        print("错误：Pillow 库未安装。")
        print("请使用 'pip install Pillow' 命令进行安装。")
        exit()

    if not os.path.exists(INPUT_IMAGE):
        print(f"错误：输入图片 '{INPUT_IMAGE}' 不存在。")
        print("请将图片文件放置在脚本相同目录下，或更新 INPUT_IMAGE 变量的路径。")
    else:
        split_image(INPUT_IMAGE, ROWS, COLS, OUTPUT_DIR)
