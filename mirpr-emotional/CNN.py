import cv2
import numpy as np
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.layers import BatchNormalization
from keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from networkx.drawing.tests.test_pylab import plt
from utils import getData, divideData, adjusted_detect_face

tensorflow.compat.v1.disable_eager_execution()
num_features = 64
num_labels = 7
batch_size = 64
epochs = 100
width, height = 64, 64

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(width, height, 1)))
model.add(Conv2D(num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(2 * num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(2 * num_features, kernel_size=(3, 3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(16 * num_features, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(num_labels, activation='softmax'))

# Compliling the model with adam optimixer and categorical crossentropy loss
model.compile(loss=categorical_crossentropy,
              optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
              metrics=['accuracy'])


def EmotionRecognition(trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet, model):
    labels = []
    data = []


    for i in range(len(trainingInputSet)):
        imagePath = trainingInputSet[i]
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (64, 64))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi_gray = adjusted_detect_face(gray,(64, 64))

        labels.append(trainingOutputSet[i])
        data.append(roi_gray)
    dataV = []
    labelsV = []

    for i in range(len(validationInputSet)):
        imagePath = validationInputSet[i]
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (64, 64))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi_gray = adjusted_detect_face(gray,(64, 64))
        labelsV.append(validationOutputSet[i])
        dataV.append(roi_gray)

    lenData = len(data)
    lenDataV = len(dataV)
    data = np.reshape(data, (lenData, 64, 64, 1))
    dataV = np.reshape(dataV, (lenDataV, 64, 64, 1))
    model.summary()
    # training the model
    history = model.fit(np.array(data), np.array(labels),
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(np.array(dataV), np.array(labelsV)),
                        shuffle=True)

    # saving the  model to be used later
    json = model.to_json()
    with open("model_v1.json", "w") as json_file:
        json_file.write(json)
    model.save_weights("model_v1.h5")
    print("Saved model to disk")

    model.compile(loss=categorical_crossentropy,
                  optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
                  metrics=['accuracy'])

    train_eval = model.evaluate(np.array(data), np.array(labels), verbose=1)
    print('Train loss:', train_eval[0])
    print('Train accuracy:', train_eval[1])

    test_eval = model.evaluate(np.array(dataV), np.array(labelsV), verbose=1)
    print('Test loss:', test_eval[0])
    print('Test accuracy:', test_eval[1])

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig("loss.jpg")


inputList, outputList = getData('sessions/**/*.jpg')
trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet = divideData(inputList, outputList)
EmotionRecognition(trainingInputSet, trainingOutputSet, validationInputSet, validationOutputSet, model)
