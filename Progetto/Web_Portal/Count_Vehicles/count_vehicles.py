import os, sys, cv2, argparse
from glob import glob
from Count_Vehicles.SSD import SSD
import numpy as np
from keras.models import load_model
import time

# def init_parameter():   
#     parser = argparse.ArgumentParser(description='Vehicle counting')
#     parser.add_argument("--nn_path", type=str, nargs='?', default='Count_Vehicles/model-final.pb', help="Path della rete.")
#     parser.add_argument("--img_path", type=str, nargs='?', default='Count_Vehicles/test.jpg', help="Path dell'immagine da elaborare.")
#     args = parser.parse_args()
#     return args

def init_net(nn_path):
    d = SSD(nn_path)
    return d

def count_vehicles(nn, img_path, threshold):
    img = cv2.imread(img_path)
    boxes, scores, classes = nn.det(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    vehicle_num = 0
    for i in range(len(scores[0])):
        if scores[0][i] > threshold:
            vehicle_num += 1
    return vehicle_num


# args = init_parameter()
# nn = init_net(args.nn_path)
# vehicle_num = count_vehicle(nn, args.img_path, 0.37)
# print("Veicoli rilevati: " + str(vehicle_num))