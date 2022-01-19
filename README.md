# EMOtional

- EMOtional- Table of content
  * [1. Introduction](#introduction)
  * [2. Why are kids challenging?](#why-are-kids-challenging)
  * [3.Classification results](#classification-results)
    + [3.1 Facial recognition](#facial-recognition)
    + [3.2 Emotion recognition](#emotion-recognition)
  * [4.How to use?](#how-to-use)
    + [4.1 Install dependencies](#install-dependencies)
  * [5.Useful links](#5useful-links)


<a name="introduction"/>

## 1. Introduction
We all know that children are very emotional and don't hesitate to express their emotion in all the activities they do. The goal of our project is to objectively measure the emotions of preschoolers
following the interaction with some educational activities. At a very young age, they still cannot give written feedback, so the best way to measure user satisfaction is observation.
Our project allows the login of a preschooler in the application and start some small interactive games after which a report of emotions is established. This report will be automatically sent to the educator.

An LBP based facial recognition algorithm was used as the login procedure and for the recognition of emotions we used a Convolutional Neural Network together with Haar Cascade Classifiers. 

The interractive application is developed in C# + VueJS 3 and integrates these previously presented smart models.

<a name="why-are-kids-challenging"/>

## 2. Why are kids challenging?

The training was performed on the [CAFE](https://nyu.databrary.org/volume/30) database. This database contains 1192 photographs of 154 children. The name of each photograph contains the emotion expressed along with a unique identifier given to each participant in the experiment.

The 7 basic emotions included in the dataset ("sadness", "happiness", "fear", "anger", "surprise", "disgust", "neutral") are not balanced, which can be seen from the following histogram .

![dataset](https://user-images.githubusercontent.com/79506808/145709101-30a54680-f3c0-4b70-872e-1bec3ce57b1f.png)


Moreover, the features of the children are not as pronounced as those of the adults and we encountered problems in determining the rectangle of the face with the Haar classifier in openCV.  To solve this problem we have chosen to manually decrease the brightness of the images before they are given for facial detection.


|Original image | Processed image|
| ------------- |:-------------:| 
|  ![gray](https://user-images.githubusercontent.com/79506808/145712463-c4f1a25a-6779-43ce-a6af-fbede4babc5a.png)      |![less_bright](https://user-images.githubusercontent.com/79506808/145712464-4c75da50-faa7-43ca-b634-bac2382c2ae7.png) |

And finally, after applying the haar classifier and resizing, an input image will look like this:
<p align="center" width="100%">
    <img width="33%" src="https://user-images.githubusercontent.com/79506808/145712811-769e90f6-b5a5-4a12-87a5-ee979af9c508.png">
</p>


<a name="classification-results"/>

## 3.Classification results

<a name="facial-recognition"/>

### 3.1 Facial recognition


For the facial recognition part, we chose [Local Binary Patterns Histogram](https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b) - an algorithm that involves labeling each pixel of an image by applying a threshold on the neighbors of a pixel and transforming the result into a binary number. The black and white image is then divided into regions. The extraction of the histogram corresponding to each region is based on the creation of a histogram with 256 positions whose value represents the number of occurrences of each value corresponding to the pixels. The histograms thus obtained are concatenated and for the facial recognition part they are compared. The easiest way to compare them is to make a Euclidean distance. 

<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/79506808/145713887-18a83553-f390-472c-b807-e641a5c1bd7e.png">
</p>


<a name="emotion-recognition"/>

### 3.2 Emotion recognition

To detect emotions we chose to use a CNN with the following architecture that receives as input each image processed and resized to 64x64 pixels :
<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/79506808/145714090-c8e77fdf-394b-40c5-9d30-80596efd049d.png">
</p>

Unfortunately, the results are not satisfactory enough, although in the last training we added Early Stopping to prevent overfitting.

|Accuracy metrics| Loss|Confusion matrix|
| ------------- |:-------------:| -------------|
|![new_acc](https://user-images.githubusercontent.com/79506808/145714415-194e0687-f5f4-4cbc-8287-62f812a6d927.png)|![loss2](https://user-images.githubusercontent.com/79506808/145714461-88eb726d-4438-4067-af2c-d061f4df63c9.jpg)|![confusion](https://user-images.githubusercontent.com/79506808/145714578-edc585a1-fea2-4d4f-9d69-15bc2d2f98a0.png)


<a name="how-to-use"/>

## 4.How to use?

<a name="install-dependencies"/>

### 4.1 Install dependencies

* numpy
* opencv
* tensorflow
* keras
* skimage

### 4.2 Application flow

After the child/ educator starts the application, a gif appears on the screen to keep the child's attention.

<p align="center" width="100%">
    <img width="70%" src="https://user-images.githubusercontent.com/79506808/145726613-348d08f1-ec53-4d7a-b0c7-f4dd4dc973d8.png">
</p>

After successful authentication, the application sends you to the main page. To the left of the main window is a list of options that contain links to interactive games

<p align="center" width="100%">
    <img width="70%" src="https://user-images.githubusercontent.com/79506808/145726789-b4119994-8140-4902-994a-2a9849565611.png">
</p>

As the child interacts with an activity, screenshots are sent back every few seconds and the predominant emotion returns. At the end of the activity a diagram is made from these emotions and it will be exported to the educator.



<a name="useful-links"/>

## 5.Useful links

1. [Emotion Detection Using OpenCV and Keras](https://medium.com/swlh/emotion-detection-using-opencv-and-keras-771260bbd7f7)
2. [Haar Cascades for Object Detection](https://www.geeksforgeeks.org/python-haar-cascades-for-object-detection/)
3. [Face Detection with HAAR Cascade](https://machinelearningknowledge.ai/face-detection-with-haar-cascade-in-opencv-python/)
4. [Understanding LBPH Algorithm](https://towardsdatascience.com/face-recognition-how-lbph-works-90ec258c3d6b)
5. [Local Binary Pattern](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_local_binary_pattern.html)
6. [LBPH algorithm for Face Recognition](https://iq.opengenus.org/lbph-algorithm-for-face-recognition/)
7. [Python integration](https://towardsdatascience.com/power-your-windows-app-with-ai-connect-c-application-with-python-model-c5f100ebc1fc)
8. [Vue JS](https://vuejs.org/v2/guide/)
9. [Entity framework](https://docs.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/models-data/creating-model-classes-with-the-entity-framework-cs)
