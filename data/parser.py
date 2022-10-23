import json
import os
from os.path import isfile, join
import numpy as np
import cv2

import argparse 

def data_aug(img, mode=0):
    """
    Аугментация изображений посредством ротации и отзеркаливания

    Args:
        img (_type_): Изображение в ndarray
        mode (int, optional): Режим изменения изображения Defaults to 0.

    Returns:
        _type_: Изображение в ndarray
    """
    
    if mode == 0:
        return img
    elif mode == 1:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif mode == 2:
        return cv2.rotate(img, cv2.ROTATE_180)
    elif mode == 3:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif mode == 4:
        return cv2.flip(img, 0)
    elif mode == 5:
        return cv2.flip(img, 1)
    elif mode == 6:
        return cv2.flip(img, -1)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input-folder', metavar='Filename', type=str, help='Path to image folder')
parser.add_argument('--input-json', metavar='Filename', type=str, help='Path to JSON with polygones')

args = parser.parse_args()
if args.input_folder is None or args.input_json is None:
    parser.print_help()
    exit(1)

print("Input image:", args.input_folder)
print("Input JSON :", args.input_json)

file = open(args.input_json)
all = json.load(file)
mypath = args.input_folder
onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

os.mkdir("dataset")
for image in onlyfiles:
    if image.split('.')[1] == 'jpg' or image.split('.')[1] == 'png':
    # Для каждого изображения в папке с разрешением jpg,png 
        for x in range(7):
    # Для каждого типа аугментации от 0 до 6
            path = "dataset/"+image.split('.')[0]+"_"+str(x)
            os.mkdir(path)

            # Создаем пукти в папке dataset
            os.mkdir(path+"/image")
            os.mkdir(path+"/masks")

            regions = all[image]['regions']

            # Читаем изображения и параллельно копируем в формате png
            imageaug = cv2.imread(image)
            imagenew = data_aug(imageaug,x)
            imagename = image.split('.')[0]+"_"+str(x)
            cv2.imwrite(os.path.join(path , f"image/{imagename}.png"), imagenew)
            #print(imageaug.shape)
            image_size = imageaug.shape[:-1]
            mask  = np.zeros((image_size[0], image_size[1], 1))

            # Для каждого региона в json файле по изображению вытаскиваем полигон.
            for i,key in enumerate(regions.keys()):
                x_points = regions[key]['shape_attributes']['all_points_x']
                y_points = regions[key]['shape_attributes']['all_points_y']
                mask  = np.zeros((image_size[0], image_size[1], 1))
                points = np.array([[x, y] for x, y in zip(x_points, y_points)])
                pts = points.reshape((-1, 1, 2))
                # Заполняем белым цветом маску на основе полигона
                cv2.fillPoly(mask, np.int32([pts]), (255, 255, 255))
                mask = data_aug(mask,x)
                cv2.imwrite(os.path.join(path , f"masks/result{i}.png"), mask)
        