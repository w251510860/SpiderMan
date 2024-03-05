#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.

import sys
import os
from PIL import Image


def split_img(path: str, base_name):
    img_names = []
    path = path if path[-1] == '/' else f'{path}/'
    file_path = path + base_name + '.png'
    im = Image.open(file_path)
    # 图片的宽度和高度
    img_size = im.size
    weight = img_size[0]
    height = img_size[1]
    y = 956
    h = 1434
    num = height // 1434
    last_height = height % 1434
    n = 0
    for i in range(num):
        n += 1
        if i == 0:
            region = im.crop((0, 450, weight, h * i + y))
        else:
            region = im.crop((0, h * i, weight, h * i + y))
        paths = file_path.replace('.png', '')
        # 文件输出位置
        region.save(f"{paths}_{i}.png")
        img_names.append(f"{base_name}_{i}")
    if img_size[1] in [2868, 5736]:
        return img_names, img_size
    # 补充最后一张图
    region = im.crop((0, h * n, weight, h * n + last_height))
    paths = file_path.replace('.png', '')
    region.save(f"{paths}_{n}.png")
    img_names.append(f"{base_name}_{n}")
    return img_names, img_size


def image_concat(path, image_names, base_name):
    path = path if path[-1] == '/' else f'{path}/'
    num = len(image_names)
    weight = []
    height = []
    img_files = []
    for name in image_names:
        img_obj = Image.open(f'{path}{name}.png')
        weight = img_obj.size[0]
        height.append(img_obj.size[1])
        img_files.append(img_obj)

    target = Image.new('RGB', (weight, sum(height)))  # 拼接前需要写拼接完成后的图片大小 1200*600
    next_height = 0
    for i in range(num):
        a = 0  # 图片距离左边的大小
        b = next_height  # 图片距离上边的大小
        c = weight  # 图片距离左边的大小 + 图片自身宽度
        d = next_height + height[i]  # 图片距离上边的大小 + 图片自身高度
        target.paste(img_files[i], box=(a, b, c, d))
        next_height = d
    target.save(path + f'{base_name}_con' + '.png')


def get_all_path(path="./target_img"):
    file_name_list = []
    for file_name in os.listdir(path):
        file_name = file_name.replace('.png', '')
        file_name_list.append(file_name)
    return file_name_list


def init(base_names, path='/Users/wangjingling/代码/SpiderMan/target_img/'):
    for base_name in base_names:
        # 删除文件
        if '_con' not in base_name:
            os.remove(path + base_name + '.png')

if __name__ == '__main__':
    path = '/target_img/'
    base_names = get_all_path(path)
    init(base_names)
    # names = []
    #
    # for base_name in base_names:
    #     try:
    #         image_names, img_size = split_img(path, base_name)
    #         image_concat(path, image_names, base_name)
    #         names.extend(image_names)
    #     except Exception:
    #         print(base_name)
    # for name in names:
    #     try:
    #         os.remove(path + name + '.png')
    #     except Exception:
    #         print(name)
    #
