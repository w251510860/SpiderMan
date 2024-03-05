#  This software shall not be used for commercial purposes, only for learning communication
#  Copyright (c) 2022-2023. All rights reserved.

import sys
import os
from PIL import Image


def split_img(path: str, base_name, save_path: str=None):
    if not save_path:
        save_path = path
    img_names = []
    path = path if path[-1] == '/' else f'{path}/'
    save_path = save_path if save_path[-1] == '/' else f'{save_path}/'
    file_path = path + base_name + '.png'
    im = Image.open(file_path)
    # 图片的宽度和高度
    img_size = im.size
    weight = img_size[0]
    height = img_size[1]
    region = im.crop((0, 250, weight, height - 1320))
    save_path = f'{save_path}{base_name}.png'
    region.save(save_path)
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


def get_all_path(path="./test"):
    file_name_list = []
    for file_name in os.listdir(path):
        file_name = file_name.replace('.png', '')
        file_name_list.append(file_name)
    return file_name_list


def init(base_names, path='/Users/wangjingling/代码/SpiderMan/HandleImg/'):
    ret_names = []
    for base_name in base_names:
        # 删除文件
        if '_1' in base_name:
            os.remove(path + base_name + '.png')
        else:
            ret_names.append(base_name)
    return ret_names

if __name__ == '__main__':
    test_path = './test/'
    path = '../../datasets/screenshot/盐城市第一人民医院-471/ori/'
    base_names = get_all_path(path)
    # base_names = init(base_names, path=path)
    names = []

    for base_name in base_names:
        if base_name[0] == '.':
            continue
        save_path = '../../datasets/screenshot/盐城市第一人民医院-471/target'
        image_names, img_size = split_img(path, base_name, save_path)
        # try:
        #     image_names, img_size = split_img(path, base_name)
        #     image_concat(path, image_names, base_name)
        #     names.extend(image_names)
        # except Exception as e:
        #     print(e)
        #     print(base_name)
    # for name in names:
    #     try:
    #         os.remove(path + name + '.png')
    #     except Exception:
    #         print(name)

