import os, sys, cv2, argparse
from glob import glob
from Count_People.SSD import SSD
import numpy as np
from keras.models import load_model
import time

# def init_parameter():   
#     parser = argparse.ArgumentParser(description='People counting')
#     parser.add_argument("--nn_path", type=str, nargs='?', default='Count_People/model-final.pb', help="Path della rete.")
#     parser.add_argument("--img_path", type=str, nargs='?', default='Count_People/test.jpg', help="Path dell'immagine da elaborare.")
#     args = parser.parse_args()
#     return args

def init_net(nn_path):
    d = SSD(nn_path)
    return d

def count_people(nn, img_path, threshold):
    img = cv2.imread(img_path)
    boxes, scores, classes = nn.det(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    people_num = 0
    for i in range(len(scores[0])):
        if scores[0][i] > threshold:
            people_num += 1
    return people_num


# args = init_parameter()
# nn = init_net(args.nn_path)
# people_num = count_people(nn, args.img_path, 0.4)
# print("Persone rilevate: " + str(people_num))