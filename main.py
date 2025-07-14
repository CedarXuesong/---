import os
from PIL import Image

def split_image_to_squares(image_path, m, n, output_dir):
    # 打开图片，确保为RGBA模式
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size

    # 创建正方形画布，边长为max(width, height)
    canvas_size = max(width, height)
    canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    # 计算居中粘贴位置
    paste_x = (canvas_size - width) // 2
    paste_y = (canvas_size - height) // 2
    canvas.paste(img, (paste_x, paste_y))

    # 分割参数
    cell_size = canvas_size // max(m, n)

    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    for row in range(m):
        for col in range(n):
            left = col * cell_size
            upper = row * cell_size
            right = left + cell_size
            lower = upper + cell_size
            crop = canvas.crop((left, upper, right, lower))
            out_path = os.path.join(output_dir, f'square_{row}_{col}.png')
            crop.save(out_path)
    print(f'已保存到 {output_dir}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='将图片分割为m行n列的正方形小图，空白区域透明填充')
    parser.add_argument('image', help='输入图片路径')
    parser.add_argument('m', type=int, help='行数')
    parser.add_argument('n', type=int, help='列数')
    parser.add_argument('--output', default='output', help='输出文件夹')
    args = parser.parse_args()
    split_image_to_squares(args.image, args.m, args.n, args.output)
