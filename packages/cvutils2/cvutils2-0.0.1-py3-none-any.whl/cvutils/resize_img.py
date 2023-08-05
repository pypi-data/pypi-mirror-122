import os

from PIL import Image


def resize(src_img_path, target_img_path, size):
    img = Image.open(src_img_path)
    img = img.resize(size)
    img.save(target_img_path)


def resize_whole_folder(src_folder, target_folder, size):
    for img_name in os.listdir(src_folder):
        resize(src_img_path=os.path.join(src_folder, img_name),
               target_img_path=os.path.join(target_folder, img_name),
               size=size)


if __name__ == '__main__':
    resize_whole_folder(src_folder=r'C:\Programs\workspace\deep_learning\data\Float\img',
                        target_folder=r'C:\Programs\workspace\deep_learning\data\Float\img_720p',
                        size=(1280, 720))
