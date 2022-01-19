import glob
from enum import Enum
from threading import Thread

import numpy as np
import cv2


class Emotions(Enum):
    Surprise = 0
    Sad = 1
    Neutral = 2
    Happy = 3
    Fear = 4
    Disgust = 5
    Angry = 6


# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix
# import itertools

# def plotConfusionMatrix(cm, classNames, title):
#     classes = classNames
#     plt.figure()
#     # plt.imshow(cm, interpolation = 'nearest', cmap = 'Blues')
#     plt.title('Confusion Matrix ' + title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classNames))
#     plt.xticks(tick_marks, classNames, rotation=45)
#     plt.yticks(tick_marks, classNames)
#
#     text_format = 'd'
#     thresh = cm.max() / 2.
#     for row, column in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(column, row, format(cm[row, column], text_format),
#                 horizontalalignment = 'center',
#                 color = 'white' if cm[row, column] > thresh else 'black')
#
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')
#     plt.tight_layout()
#
#     plt.show()
#
# def evalMultiClass(realLabels, computedLabels, labelNames):
#     from sklearn.metrics import confusion_matrix
#
#     confMatrix = confusion_matrix(realLabels, computedLabels)
#     acc = sum([confMatrix[i][i] for i in range(len(labelNames))]) / len(realLabels)
#     precision = {}
#     recall = {}
#     for i in range(len(labelNames)):
#         precision[labelNames[i]] = confMatrix[i][i] / sum([confMatrix[j][i] for j in range(len(labelNames))])
#         recall[labelNames[i]] = confMatrix[i][i] / sum([confMatrix[i][j] for j in range(len(labelNames))])
#     return acc, precision, recall, confMatrix

def getDataTesting(path):
    images = glob.glob(path, recursive=True)
    sorted_images = {}
    input = []
    output = []
    inputEmo = []
    outputEmo = []
    for image in images:
        unique_id = image.split('_')[1].split('.')[0]
        input.append(image)
        output.append(unique_id)
        inputEmo.append(image)
        if 'surprise' in image:
            outputEmo.append([1, 0, 0, 0, 0, 0, 0])
        if 'sad' in image:
            outputEmo.append([0, 1, 0, 0, 0, 0, 0])
        if 'neutral' in image:
            outputEmo.append([0, 0, 1, 0, 0, 0, 0])
        if 'happy' in image:
            outputEmo.append([0, 0, 0, 1, 0, 0, 0])
        if 'fear' in image:
            outputEmo.append([0, 0, 0, 0, 1, 0, 0])
        if 'disgust' in image:
            outputEmo.append([0, 0, 0, 0, 0, 1, 0])
        if 'angry' in image:
            outputEmo.append([0, 0, 0, 0, 0, 0, 1])
        if unique_id in sorted_images.keys():
            sorted_images[unique_id].append(image)
        else:
            sorted_images[unique_id] = []
            sorted_images[unique_id].append(image)

    return input, output


def getData(path):
    images = glob.glob(path, recursive=True)
    sorted_images = {}
    input = []
    output = []
    inputEmo = []
    outputEmo = []
    for image in images:
        unique_id = image.split('_')[1].split('.')[0]
        input.append(image)
        output.append(unique_id)
        inputEmo.append(image)
        if 'surprise' in image:
            outputEmo.append([1, 0, 0, 0, 0, 0, 0])
        if 'sad' in image:
            outputEmo.append([0, 1, 0, 0, 0, 0, 0])
        if 'neutral' in image:
            outputEmo.append([0, 0, 1, 0, 0, 0, 0])
        if 'happy' in image:
            outputEmo.append([0, 0, 0, 1, 0, 0, 0])
        if 'fear' in image:
            outputEmo.append([0, 0, 0, 0, 1, 0, 0])
        if 'disgust' in image:
            outputEmo.append([0, 0, 0, 0, 0, 1, 0])
        if 'angry' in image:
            outputEmo.append([0, 0, 0, 0, 0, 0, 1])
        if unique_id in sorted_images.keys():
            sorted_images[unique_id].append(image)
        else:
            sorted_images[unique_id] = []
            sorted_images[unique_id].append(image)

    return inputEmo, outputEmo


def divideData(input, output):
    np.random.seed(5)
    indexes = [i for i in range(len(input))]
    trainSample = np.random.choice(indexes, int(0.8 * len(input)), replace=False)
    testSample = [i for i in indexes if not i in trainSample]

    trainingInputSet = [input[i] for i in trainSample]
    trainingOutputSet = [output[i] for i in trainSample]
    validationInputSet = [input[i] for i in testSample]
    validationOutputSet = [output[i] for i in testSample]

    return trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet


def run_euc(list_a, list_b):
    sum = 0
    for i in range(len(list_a)):
        sum += (list_b[i] - list_a[i]) ** 2
    return sum

def adjusted_detect_face(img,dimTuple):
    face_img = img.copy()
    facecasc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_rect = facecasc.detectMultiScale(face_img,
                                          scaleFactor=1.2,
                                          minNeighbors=5)
    roi_gray = face_img
    id = 0
    for (x, y, w, h) in face_rect:
        cv2.rectangle(face_img, (x, y),
                      (x + w, y + h), (255, 255, 255), 10)
        roi_gray = face_img[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, dimTuple)
        id +=1

    return roi_gray

def adjusted_detect_face(img, dimTuple, detectionType):
    face_img = img.copy()
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    gray = decrease_brightness(gray, 50)
    facecasc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_rect = facecasc.detectMultiScale(gray,
                                          scaleFactor=1.2,
                                          minNeighbors=5)
    roi_gray = gray
    for (x, y, w, h) in face_rect:
        cv2.rectangle(gray, (x, y),
                      (x + w, y + h), (255, 255, 255), 10)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, dimTuple)
        break

    if detectionType == "emotion":
        backtorgb = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2RGB)
        data = np.reshape(backtorgb, (1, 64, 64, 3))
        return data
    return roi_gray


def decrease_brightness(image, value):
    nrOfThreads = 8
    threads = []
    nrOfLines = len(image) // nrOfThreads
    remainingLines = len(image) % nrOfThreads
    for i in range(nrOfThreads):
        t = Thread(target=onLines, args=[image, i * nrOfLines, nrOfLines, value])
        t.start()
        threads.append(t)
    for i in range(len(image) - remainingLines, len(image)):
        for j in range(len(image[i])):
            if image[i][j] - value > 0:
                image[i][j] -= value
    for t in threads:
        t.join()
    return image


def onLines(image, line, nrOfLines, value):
    for i in range(line, line + nrOfLines):
        for j in range(len(image[i])):
            if image[i][j] - value > 0:
                image[i][j] -= value
