import cv2
import numpy as np
import pandas as pd
import os.path
from sklearn.neighbors import KNeighborsClassifier

#Encontre dentro de un texto que Knn en reconocimiento facial es muy acertado cuando se presentan rostros descubiertos,
#sin embargo, su precision cae drasticamente cuando se presenta un objeto como lentes, barba, cabello
#o alguna posicion que no permita ver el rostro completamente de frente y con una buena iluminacion

fileName = "faceData.csv"
preName = "s"
classifier = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")


def main(args, fileName):
    for subject in range(40):
        subjectName = preName + str(subject + 1)
        facesAsList = []
        print("Generando valores correspondientes a el sujeto %s" % (str(subject + 1)))
        for image in range(10):
            selection = cv2.imread("./archive/s%s/%s.pgm" % (str(subject+1),str(image+1)))
            detectedFaces = classifier.detectMultiScale(selection, 1.5, 5)
            print("Detectando rostros")
            #print(detectedFaces)
            sorted(detectedFaces, key = lambda x: x[2]*x[3],reverse = True)
            print("Ordenando rostros detectados")
            print(detectedFaces)
            print(len(detectedFaces))
            if len(detectedFaces) == 1:
                x, y, w, h = detectedFaces[0]
                print("X=%s, Y=%s, W=%s, H=%s" % (x, y, w, h))
                imageFrame = selection[y:y + h, x:x + w]
                #cv2.imshow("face", imageFrame)
                imageToSave = cv2.resize(imageFrame, (100,100))
                print(len(facesAsList), type(imageFrame), imageFrame.shape)
                facesAsList.append(imageToSave.reshape(-1))
            else:
                x, y, w, h = [0,0,92,112]
                imageFrame = selection[y:y + h, x:x + w]
                imageToSave = cv2.resize(imageFrame, (100,100))
                print(len(facesAsList), type(imageFrame), imageFrame.shape)
                print("X=%s, Y=%s, W=%s, H=%s" % (x, y, w, h))
                facesAsList.append(imageToSave.reshape(-1))
        print("Tamanio de lista de rostros a ligar con el sujeto %s: %s" % (str(subject + 1),len(facesAsList)))
        print("Almacenando datos en archivo csv")
        #saveDataInCSV(subjectName, np.array(facesAsList))
    print("Iniciando reconocimiento facial")
    recognizeFace(fileName)

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
            cv2.rectangle(imageToEvaluate, (x,y), (x + w, y + h), (255,0,0), 3)
            cv2.putText(imageToEvaluate, response[i], (x-50, y-50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)
    else:
        x, y, w, h = [0,0,92,112]
        foundFace = imageToEvaluate[y:y + h, x:x + w]
        foundFace = cv2.resize(foundFace, (100,100))
        XTest.append(foundFace.reshape(-1))
        response = model.predict(np.array(XTest))
        cv2.rectangle(imageToEvaluate, (x,y), (x + w, y + h), (255,0,0), 3)
        cv2.putText(imageToEvaluate, response[0], (x-50, y-50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)
    print("Sujeto predecido es: %s" % (response[0]))
    cv2.imshow("Sujeto predecido", imageToEvaluate)
    predictedImage = cv2.imread("./archive/%s/1.pgm" % (response[0]))
    cv2.imshow("Sujeto seleccionado", predictedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Eliminando archivo csv para actualizacion futura...")
    #os.remove("./%s" % (fileName))
    print("Eliminacion exitosa, cuando se vuelva a ejecutar el algoritmo se volvera a generar este archivo")


if __name__ == '__main__':
    main()