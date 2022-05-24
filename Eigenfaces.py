from numpy.lib.npyio import load
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from skimage.exposure import rescale_intensity
from sklearn.metrics import accuracy_score
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import loadingFaces


def main(args, fileName):
    print("Inicializando deteccion con algoritmo Eigenfaces")
    (faces, labels) = loadingFaces.loadDataSet()
    print("Las imagenes de la base de datos han sido cargadas")
    pcaFaces = np.array([f.flatten() for f in faces])
    print("Longitud de pcaFaces")
    print(len(pcaFaces))
    le = LabelEncoder()
    #print("Etiquetas de imagenes antes de transformacion")
    #print(labels)
    labels = le.fit_transform(labels)
    labels.sort()
    print("Etiquetas de imagenes despues de transformacion")
    print(len(labels))
    print(labels)
    print()
    split = train_test_split(faces, pcaFaces, labels, test_size=0.25, stratify=labels, random_state=42)
    (origTrain, origTest, trainX, testX, trainY, testY) = split
    print(testY)
    print("Cantidad de imagenes en test %s" % (len(origTest)))
    print("Construyendo eigenfaces")
    pca = PCA(svd_solver="randomized", n_components=300, whiten=True)
    start = time.time()
    trainX = pca.fit_transform(trainX)
    end = time.time()
    print("El tiempo del calculo de eigenfaces tomo {:.4f} segundos".format(end-start))
    images = []
    print("Numero de componentes: %s Numero de features: %s" % (pca.n_components_,pca.n_features_))
    for (i, component) in enumerate(pca.components_[:40]):
        component = component.reshape((112, 276))
        component = rescale_intensity(component, out_range=(0,255))
        component = np.dstack([component.astype("uint8")] * 3)
        images.append(component)

    print("Numero de imagenes %s" % (len(images)))
    display = imutils.build_montages(images, (56, 138), (10,4))[0]

    media = pca.mean_.reshape((112, 276))
    media = rescale_intensity(media, out_range=(0,255))
    #cv2.imshow("Media", media)
    #cv2.imshow("Componentes", display)
    #cv2.waitKey(0)

    print("Imprimiendo testX")
    print(testX)
    print("Imprimiendo testY")
    print(testY)

    print("Iniciando entrenamiento de clasificador")
    model = SVC(kernel="linear", C=10.0, gamma=0.001, random_state=42)
    model2 = SVC(kernel="sigmoid", C=10.0, gamma=0.001, random_state=42)
    model.fit(trainX,trainY)
    model2.fit(trainX,trainY)
    imageToEvaluate = []
    imageToEvaluate.append(cv2.imread(fileName))
    imageToEvaluate = np.array([image.flatten() for image in imageToEvaluate])
    imageToEvaluate.reshape(1,-1)
    imageToEvaluate = imageToEvaluate[:, :300]
    print("Forma de imagen a evaluar ", imageToEvaluate.shape)
    start = time.time()
    response = model.predict(imageToEvaluate)
    response2 = model2.predict(imageToEvaluate)
    end = time.time()
    print("Valor de respuesta %s" % (str(response[0])))
    responseName = le.inverse_transform(response)[0]
    responseName2 = le.inverse_transform(response2)[0]
    responseSubjectImage = cv2.imread("./archive/s%s/1.pgm" % (str(response[0])))
    responseSubjectImage2 = cv2.imread("./archive/s%s/2.pgm" % (str(response2[0])))
    responseImage = images[int(str(response[0]))]
    responseImage2 = images[int(str(response2[0]))]
    responseSubjectImageResized = cv2.resize(responseSubjectImage, (112,112))
    responseSubjectImageResized2 = cv2.resize(responseSubjectImage2, (112,112))
    responseImageResized = cv2.resize(responseImage, (112,112))
    responseImageResized2 = cv2.resize(responseImage2, (112,112))
    expectedImage = cv2.imread(fileName)
    expectedImage = cv2.resize(expectedImage, (112,112))
    
    #cv2.imshow("Imagen evaluada", expectedImage)
    #cv2.imshow("Imagen respuesta con cv2", responseSubjectImageResized)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    print("prediccion: {}, valor esperado: {}".format(responseName, "Sujeto 1"))

    print("Evaluando el modelo")
    predicciones = model.predict(pca.transform(testX))
    print("Reporte de precision para conjunto sin alteraciones")

    resultingTime = end-start
    return (responseSubjectImageResized, resultingTime, ("Sujeto " + str(response[0])), responseSubjectImageResized2, ("Sujeto " + str(response2[0])))

distortions = ['_brightness_','_distortion_affine1_', '_distortion_affine2_', '_distortion_arc1_', '_distortion_arc2_', '_scale_']

def testingMatrix():
    generalScores = []
    print("Inicializando deteccion con algoritmo Eigenfaces")
    (faces, labels) = loadingFaces.loadDataSet()
    pcaFaces = np.array([f.flatten() for f in faces])
    print("Las imagenes de la base de datos han sido cargadas")
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels.sort()
    split = train_test_split(faces, pcaFaces, labels, test_size=0.25, stratify=labels, random_state=42)
    (origTrain, origTest, trainX, testX, trainY, testY) = split
    pca = PCA(svd_solver="randomized", n_components=300, whiten=True)
    trainX = pca.fit_transform(trainX)
    for (i, component) in enumerate(pca.components_[:40]):
            component = component.reshape((112, 276))
            component = rescale_intensity(component, out_range=(0,255))
            component = np.dstack([component.astype("uint8")] * 3)
    model = SVC(kernel="linear", C=10.0, gamma=0.001, random_state=42)
    model.fit(trainX,trainY)
    print("Evaluando el modelo")
    predicciones = model.predict(pca.transform(pcaFaces))
    print("Precision sin alteraciones")
    print(accuracy_score(labels,predicciones))
    generalScores.append(accuracy_score(labels,predicciones))
    for distortion in distortions:
        (faces2, labels2) = loadingFaces.loadModifiedDataSetNew(distortion)
        print("Tamanio de caras cargadas %s" % (len(faces2)))
        pcaModiefiedFaces = np.array([f.flatten() for f in faces2])
        labels2 = le.fit_transform(labels2)
        labels2.sort()
        prediccionesMod = model.predict(pca.transform(pcaModiefiedFaces))
        print("Precision con distorsion %s" % (distortion))
        print(accuracy_score(labels2,prediccionesMod))
        generalScores.append(accuracy_score(labels2,prediccionesMod))
        for x in prediccionesMod:
            predicciones = np.append(predicciones, x)
    return generalScores, predicciones

if __name__ == '__main__':
    main()

