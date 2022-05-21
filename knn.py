import cv2
import numpy as np
import pandas as pd
import os.path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from skimage.exposure import rescale_intensity
from sklearn.metrics import accuracy_score
import time
import loadingFaces
from sklearn.preprocessing import LabelEncoder

fileName = "faceData.csv"
classifier = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")


def main(args, fileName):
    for subject in range(40):
        subjectName = str(subject + 1)
        facesAsList = []
        print("Generando valores correspondientes a el sujeto %s" % (str(subject + 1)))
        print("Detectando rostros")
        for image in range(10):
            selection = cv2.imread("./archive/s%s/%s.pgm" % (str(subject+1),str(image+1)))
            detectedFaces = classifier.detectMultiScale(selection, 1.5, 5)
            
            #print(detectedFaces)
            sorted(detectedFaces, key = lambda x: x[2]*x[3],reverse = True)

            #print(detectedFaces)
            #print(len(detectedFaces))
            if len(detectedFaces) == 1:
                x, y, w, h = detectedFaces[0]
                #print("X=%s, Y=%s, W=%s, H=%s" % (x, y, w, h))
                imageFrame = selection[y:y + h, x:x + w]
                #cv2.imshow("face", imageFrame)
                imageToSave = cv2.resize(imageFrame, (100,100))
                #print(len(facesAsList), type(imageFrame), imageFrame.shape)
                facesAsList.append(imageToSave.reshape(-1))
            else:
                x, y, w, h = [0,0,92,112]
                imageFrame = selection[y:y + h, x:x + w]
                imageToSave = cv2.resize(imageFrame, (100,100))
                #print(len(facesAsList), type(imageFrame), imageFrame.shape)
                #print("X=%s, Y=%s, W=%s, H=%s" % (x, y, w, h))
                facesAsList.append(imageToSave.reshape(-1))
        #print("Tamanio de lista de rostros a ligar con el sujeto %s: %s" % (str(subject + 1),len(facesAsList)))
        print("Ordenando rostros detectados")
        print("Almacenando datos en archivo csv")
        #saveDataInCSV(subjectName, np.array(facesAsList))
    print("Iniciando reconocimiento facial")
    return recognizeFace(fileName)


def saveDataInCSV(name, data):
    if os.path.isfile(fileName):
        df = pd.read_csv(fileName, index_col=0)
        latest = pd.DataFrame(data, columns=map(str,range(30000)))
        latest["name"] = name
        df = pd.concat((df,latest), ignore_index=True, sort=False)
    else:
        df = pd.DataFrame(data, columns=map(str,range(30000)))
        df["name"] = name
    df.to_csv(fileName)

def recognizeFace(imageToRecognizePath):
    start = time.time()
    data = pd.read_csv(fileName).values
    X, Y = data[:, 1:-1], data[:, -1]
    print(X,Y)
    print("Generando modelo de clasificador K-NN")
    model = KNeighborsClassifier(n_neighbors=5)
    print("Ajustando modelo")
    model.fit(X,Y)
    imageToEvaluate = cv2.imread(imageToRecognizePath)
    print("Detectando rostro en imagen proporcionada")
    facesInImage = classifier.detectMultiScale(imageToEvaluate, 1.5, 5)
    XTest = []
    if len(facesInImage) > 1:
        for face in facesInImage:
            x, y, w, h = face
            foundFace = imageToEvaluate[y:y + h, x:x + w]
            foundFace = cv2.resize(foundFace, (100,100))
            XTest.append(foundFace.reshape(-1))
        response = model.predict(np.array(XTest))
        for i, face in enumerate(facesInImage):
            x, y, w, h = face
            #cv2.rectangle(imageToEvaluate, (x,y), (x + w, y + h), (255,0,0), 3)
            #cv2.putText(imageToEvaluate, response[i], (x-50, y-50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)
    else:
        x, y, w, h = [0,0,92,112]
        foundFace = imageToEvaluate[y:y + h, x:x + w]
        foundFace = cv2.resize(foundFace, (100,100))
        XTest.append(foundFace.reshape(-1))
        response = model.predict(np.array(XTest))
        #cv2.rectangle(imageToEvaluate, (x,y), (x + w, y + h), (255,0,0), 3)
        #cv2.putText(imageToEvaluate, response[0], (x-50, y-50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)
    print("Sujeto predecido es: %s" % (response[0]))
    end = time.time()
    #cv2.imshow("Sujeto predecido", imageToEvaluate)
    predictedImage = cv2.imread("./archive/s%s/1.pgm" % (response[0]+1))
    #cv2.imshow("Sujeto seleccionado", predictedImage)
    imageToEvaluate = cv2.resize(imageToEvaluate, (112,112), interpolation = cv2.INTER_AREA)
    sideBySide = np.concatenate((imageToEvaluate, predictedImage), axis=1)
    cv2.putText(img=sideBySide, text="KNN", org=(0,0), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    #cv2.imshow("resultado", sideBySide)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    print("Eliminando archivo csv para actualizacion futura...")
    #os.remove("./%s" % (fileName))
    print("Eliminacion exitosa, cuando se vuelva a ejecutar el algoritmo se volvera a generar este archivo")
    
    return predictedImage, (end-start), response[0]+1

def evaluatingPhoto(imageToEvaluate):
    start = time.time()
    data = pd.read_csv(fileName).values
    X, Y = data[:, 1:-1], data[:, -1]
    #print(X,Y)
    #print("Generando modelo de clasificador K-NN")
    model = KNeighborsClassifier(n_neighbors=5)
    #print("Ajustando modelo")
    model.fit(X,Y)
    #print("Detectando rostro en imagen proporcionada")
    facesInImage = classifier.detectMultiScale(imageToEvaluate, 1.5, 5)
    XTest = []
    if len(facesInImage) > 1:
        for face in facesInImage:
            x, y, w, h = face
            foundFace = imageToEvaluate[y:y + h, x:x + w]
            foundFace = cv2.resize(foundFace, (100,100))
            XTest.append(foundFace.reshape(-1))
        response = model.predict(np.array(XTest))
        for i, face in enumerate(facesInImage):
            x, y, w, h = face
    else:
        x, y, w, h = [0,0,92,112]
        foundFace = imageToEvaluate[y:y + h, x:x + w]
        foundFace = cv2.resize(foundFace, (100,100))
        XTest.append(foundFace.reshape(-1))
        response = model.predict(np.array(XTest))
    #print("Sujeto predecido es: %s" % (response[0]))
    #imageToEvaluate = cv2.resize(imageToEvaluate, (112,112), interpolation = cv2.INTER_AREA)
    return response[0]

distortions = ['_brightness_','_distortion_affine1_', '_distortion_affine2_', '_distortion_arc1_', '_distortion_arc2_', '_scale_']

def testingMatrix():
    generalScores = []
    (faces, labels) = loadingFaces.loadDataSet()
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels.sort()
    split = train_test_split(faces, faces, labels, test_size=0.10, stratify=labels, random_state=42)
    (origTrain, origTest, trainX, testX, trainY, testY) = split
    predicciones = []
    print("Tamanio de TestX: %s Tamanio de TextY: %s" % (len(testX), len(testY)))
    print("Tamanio de clases %s" % (len(le.classes_)))
    print(le.classes_)
    print(testY)
    for face in testX:
        result = evaluatingPhoto(face)
        print("Imagen predecida %s" % (result))
        predicciones.append(result)
    print("Precision sin distorsion")
    print(accuracy_score(testY, predicciones))
    generalScores.append(accuracy_score(testY, predicciones))
    for distortion in distortions:
        (faces2, labels2) = loadingFaces.loadModifiedDataSetNew(distortion)
        labels2 = le.fit_transform(labels2)
        labels2.sort()
        prediccionesMod = []
        for face in faces2:
            #cv2.imshow('Rostro a evaluar', face)
            result = evaluatingPhoto(face)
            print("Imagen predecida %s" % (result))
            prediccionesMod.append(result)
            predicciones.append(result)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
        print("Precision con distorsion %s" % (distortion))
        print(accuracy_score(labels2, prediccionesMod))
        generalScores.append(accuracy_score(labels2, prediccionesMod))
    return generalScores, predicciones



if __name__ == '__main__':
    main()