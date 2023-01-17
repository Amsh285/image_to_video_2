# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 14:51:09 2023

@author: mgold
"""
import cv2
import os

image_folder = 'mandy_pngs'
video_name = 'video.mp4'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]


orig_h=320
orig_w=720
i=0
for img_crop in images[::10]:
    img = cv2.imread(os.path.join(image_folder, img_crop))
    img = img[0:orig_h, int(orig_w/2-160):int(orig_w/2+160)]
    #img = cv2.resize(crop_img, (256,256))
    num = str(i).zfill(5)
    cv2.imwrite(num+'.png', img)
    i+=1

