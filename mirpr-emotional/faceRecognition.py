import random

import cv2
from LBP import LocalBinaryPatterns
from utils import *
import sys
from utils import run_euc


# def testFaceRecognition(trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet):
#     desc = LocalBinaryPatterns(8, 1, 64)
#     labels = []
#     data = []
#     for i in range(len(trainingInputSet)):
#         imagePath = trainingInputSet[i]
#         image = cv2.imread(imagePath)
#         image = cv2.resize(image, (512, 512))
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         hist = desc.describe(gray)
#         labels.append(trainingOutputSet[i])
#         data.append(hist)
#     correct = 0
#     for i in range(len(validationInputSet)):
#         truth = validationOutputSet[i]
#         image = cv2.imread(validationInputSet[i])
#         image = cv2.resize(image, (512, 512))
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         hist = desc.describe(gray)
#         hist = np.array(hist)
#         min_dist = sys.maxsize
#         computed_truth = ""
#         for j in range(len(data)):
#             el = data[j]
#             dist = run_euc(hist, np.array(el))
#             if dist < min_dist:
#                 min_dist = dist
#                 computed_truth = labels[j]
#         if truth == computed_truth:
#             correct += 1
#     print("Accuracy on testing:" + str(correct / len(validationInputSet)))


def testFaceRecognition2(trainingInputSet, trainingOutputSet, inputImage):
    desc = LocalBinaryPatterns(8, 1, 64)
    labels = []
    data = []
    for i in range(len(trainingInputSet)):
        imagePath = trainingInputSet[i]
        image = cv2.imread(imagePath)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi_gray = adjusted_detect_face(image, (512, 512), "face")
        hist = desc.describe(roi_gray)
        labels.append(trainingOutputSet[i])
        data.append(hist)
    imagePath = inputImage
    image = cv2.imread(imagePath)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    roi_gray = adjusted_detect_face(image, (512,512), "face")
    cv2.imwrite("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\haar_pics\\" + str(random.randint(1, 20000)) + ".jpg", roi_gray)
    hist = desc.describe(roi_gray)
    hist = np.array(hist)
    min_dist = sys.maxsize
    computed_truth = ""
    for j in range(len(data)):
        el = data[j]
        dist = run_euc(hist, np.array(el))
        if dist < min_dist:
            min_dist = dist
            computed_truth = labels[j]
    return {"name": computed_truth}
