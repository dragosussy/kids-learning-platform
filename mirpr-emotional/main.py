import json
import sys
import numpy

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.optimizer_v2.adam import Adam

import cv2
import tensorflow
import warnings

from keras.losses import categorical_crossentropy
from keras.models import model_from_json

from faceRecognition import  testFaceRecognition2
from utils import *

# numpy.set_printoptions(threshold=sys.maxsize)
# inputList, outputList = getData('sessions/**/*.jpg')
# trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet = divideData(inputList, outputList)
#
# tensorflow.compat.v1.disable_eager_execution()
# json_file = open('model_v1.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# loaded_model.load_weights("model_v1.h5")
#
# dataV = []
# labelsV = []
# facecasc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#
# for i in range(len(validationInputSet)):
#     imagePath = validationInputSet[i]
#     image = cv2.imread(imagePath)
#     image = cv2.resize(image, (64, 64))
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     roi_gray = adjusted_detect_face(gray,(64,64))
#     labelsV.append(validationOutputSet[i])
#     dataV.append(roi_gray)
#
# lenDataV = len(dataV)
# dataV = np.reshape(dataV, (lenDataV, 64, 64, 1))
# loaded_model.compile(loss=categorical_crossentropy,
#                      optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
#                      metrics=['accuracy'])
# # y_predicted = loaded_model.predict(np.array(dataV))
# # outputNames = ["happy","sad","angry","disgust","neutral","surprisa","fearful"]
# # acc, prec, recall, cm = evalMultiClass(np.array(dataV), y_predicted, outputNames)
# # plotConfusionMatrix(cm, outputNames, "Emotion classification")
# #
# # print('acc: ', acc)
# # print('precision: ', prec)
# # print('recall: ', recall)
#
# test_eval = loaded_model.evaluate(np.array(dataV), np.array(labelsV), verbose=1)
# print('Test loss:', test_eval[0])
# print('Test accuracy:', test_eval[1])

# testFaceRecognition(trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet)
from utils import getDataTesting

def testEmotionDetection(imagePath):
    # tensorflow.compat.v1.disable_eager_execution()
    json_file = open('E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\efficient_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\efficient_model.h5")

    loaded_model.compile(optimizer=Adam(learning_rate=1e-3),
                         loss='categorical_crossentropy',
                         metrics=['accuracy'])

    # img = cv2.imread("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\test_sad_dragos.jpg")
    img = cv2.imread(imagePath)
    img = adjusted_detect_face(img, (64, 64), "emotion")
    prediction = loaded_model.predict(img)
    classes = np.argmax(prediction, axis=1)

    result = Emotions(classes[0]).name
    return {"emotion": result}

class MainWrapper:
    def __init__(self):
        numpy.set_printoptions(threshold=sys.maxsize)
        self.inputList, self.outputList = getDataTesting("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\poze\\*.jpg")

    def runFacialRecognition(self, jsonArguments):
        with(open("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\test-face.txt", 'w')) as f:
            f.write("ceaw din face hehe")
            f.write(jsonArguments)


        args = json.loads(jsonArguments)
        testImagePath = args['modelInput']['imagePath']
        return json.dumps(testFaceRecognition2(self.inputList, self.outputList, testImagePath))

    def runEmotionDetection(self, jsonArguments):
        with(open("E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\test-emo.txt", 'w')) as f:
            f.write("ceaw din emo hehe")
            f.write(jsonArguments)

        args = json.loads(jsonArguments)

        testImagePath = args['modelInput']['imagePath']
        return json.dumps(testEmotionDetection(testImagePath))


if (__name__ == "__main__"):
    main = MainWrapper()
    # print(main.runFacialRecognition("{\"modelInput\": {\"imagePath\": \"test_happy_dragos.jpg\"}}"))

    # args = {
    #    "modelInput": {
    #        "imagePath": "E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\emotional-backend\\emotional-backend\\temp_emotion_recog_images\\test.jpg"
    #    }
    # }
    print(main.runEmotionDetection("{\"modelInput\": {\"imagePath\": \"test_sad_dragos.jpg\"}}"))
    # print(main.runEmotionDetection(json.dumps(args)))
