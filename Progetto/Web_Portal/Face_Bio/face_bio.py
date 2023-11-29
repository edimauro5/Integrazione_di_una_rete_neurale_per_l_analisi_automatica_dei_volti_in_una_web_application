import os
import sys
import cv2
import argparse
from glob import glob
from Face_Bio.SSD import SSD
import numpy as np
from keras.models import load_model
from Face_Bio.mobilenet_v2_keras import MobileNetv2, relu6, age_relu
import time

# def init_parameter():
#     parser = argparse.ArgumentParser(description='Face counting')
#     parser.add_argument("--img_path", type=str, nargs='?', default='Face_Bio/donna.jpg', help="Path dell'immagine da elaborare.")
#     parser.add_argument("--detector", type=str, default="Face_Bio/detector.pb", help="Path del detector")
#     parser.add_argument("--gender", type=str, default="Face_Bio/gender.hdf5", help="Path del classificatore per il genere")
#     parser.add_argument("--age", type=str, default="Face_Bio/age.hdf5", help="Path del classificatore per l'età")
#     parser.add_argument("--ethnicity", type=str, default="Face_Bio/ethnicity.hdf5", help="Path del classificatore per l'etnia")
#     parser.add_argument("--emotion", type=str, default="Face_Bio/emotion.hdf5", help="Path del classificatore per l'emozione")
#     args = parser.parse_args()
#     return args


def init_net(detector, gender, age, ethnicity, emotion):
    d = SSD(detector)
    gender_classifier = load_model(gender, custom_objects={
                                   'relu6': relu6}, compile=False)
    age_classifier = load_model(
        age, custom_objects={'age_relu': age_relu}, compile=False)
    ethnicity_classifier = load_model(ethnicity, custom_objects={
                                      'relu6': relu6}, compile=False)
    emotion_classifier = load_model(emotion, compile=False)
    shape = (1, 96, 96, 3)
    gender_labels = ['F', 'M']
    ethnicity_labels = ['Afro-Americana', 'Est-Asiatica',
                        'Caucaso-Latina', 'Asiatico-Indiana']
    emotion_labels = ['Sorpresa', 'Paura', 'Disgusto',
                      'Gioia', 'Tristezza', 'Rabbia', 'Neutrale']
    return d, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier, shape, gender_labels, ethnicity_labels, emotion_labels


def get_containing_square(img, p1, p2, width, height):
    tl = [0, 0]
    br = [0, 0]
    h_img, w_img, c_img = img.shape
    max_dim = max(height, width)
    offw = max_dim - width
    offh = max_dim - height
    # Compute the containing square
    tl[0] = max(0, int(p2[0]-offw/2))
    tl[1] = max(0, int(p2[1]-offh/2))
    w = max_dim
    h = max_dim
    outx = max(0, tl[0]+w-w_img)
    outy = max(0, tl[1]+h-h_img)
    w -= outx
    h -= outy
    br[0] = tl[0]+w
    br[1] = tl[1]+h

    return tuple(br), tuple(tl), w, h


def set_color_and_size(roi, shape):
    vgg_means = [131.0912, 103.8827, 91.4953]
    input_img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    input_img = cv2.resize(
        input_img, (shape[1], shape[2]), 0, 0, cv2.INTER_LINEAR)
    input_img = np.array(input_img.astype(float)-vgg_means)
    input_img = input_img.reshape(shape)
    return input_img


def classify_faces(detector, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier, img_path, threshold, shape, gender_labels, ethnicity_labels, emotion_labels):
    img = cv2.imread(img_path)
    boxes, scores, classes = detector.det(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    gender = None
    age = None
    ethnicity = None
    emotion = None
    detected = False
    for i in range(len(scores[0])):
        if scores[0][i] > threshold and not detected:
            detected = True
            box = list(boxes[0][i]*np.array(list(img.shape[0:2])*2))
            box.reverse()
            # Bottom right
            p1 = tuple([int(a) for a in box[0:2]])
            # Top left
            p2 = tuple([int(a) for a in box[2:4]])
            w = p1[0] - p2[0]
            h = p1[1] - p2[1]
            # Face Preprocessing
            p1, p2, w, h = get_containing_square(img, p1, p2, w, h)
            roi = img[p2[1]:p1[1], p2[0]:p1[0]]
            input_img = set_color_and_size(roi, shape)
            # Gender recognition
            g_pred = gender_classifier.predict(input_img, 1, verbose=1)
            gender = int(np.argmax(g_pred, axis=1))
            # Age estimation
            age = int(age_classifier.predict(input_img, 1, verbose=1))
            print(age_classifier.predict(input_img, 1, verbose=1))
            # Ethnicity recognition
            et_pred = ethnicity_classifier.predict(input_img/255, 1, verbose=1)
            ethnicity = int(np.argmax(et_pred, axis=1))
            # Emotion recognition
            em_pred = emotion_classifier.predict(input_img, 1, verbose=1)
            emotion = int(np.argmax(em_pred, axis=1))
        elif not detected:
            return 0, "N/D", "N/D", "N/D"
    return age, gender_labels[gender], ethnicity_labels[ethnicity], emotion_labels[emotion]


# args = init_parameter()
# nn, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier, shape, gender_labels, ethnicity_labels, emotion_labels = init_net(args.detector, args.gender, args.age, args.ethnicity, args.emotion)
# gender, age, ethnicity, emotion = classify_faces(nn, gender_classifier, age_classifier, ethnicity_classifier, emotion_classifier, args.img_path, 0.4, shape, gender_labels, ethnicity_labels, emotion_labels)
# print("Gender: " + str(gender))
# print("Age: " + str(age))
# print("Ethnicity: " + str(ethnicity))
# print("Emotion: " + str(emotion))
