import os, sys, cv2, argparse
from glob import glob
from Count_Faces.SSD import SSD
import numpy as np
from keras.models import load_model
import time

# def init_parameter():   
#     parser = argparse.ArgumentParser(description='Face counting')
#     parser.add_argument("--nn_path", type=str, nargs='?', default='IC_dj/Count_Faces/model-final.pb', help="Path della rete.")
#     parser.add_argument("--img_path", type=str, nargs='?', default='IC_dj/Count_Faces/test.jpg', help="Path dell'immagine da elaborare.")
#     args = parser.parse_args()
#     return args

def init_net(nn_path):
    d = SSD(nn_path)
    return d

def count_faces(nn, img_path, threshold):
    img = cv2.imread(img_path)
    boxes, scores, classes = nn.det(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face_num = 0
    for i in range(len(scores[0])):
        if scores[0][i] > threshold:
            face_num += 1
    return face_num


# args = init_parameter()
# nn = init_net(args.nn_path)
# face_num = count_faces(nn, args.img_path, 0.4)
# print("Facce rilevate: " + str(face_num))