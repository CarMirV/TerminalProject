import cv2
import time
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import loadingFaces

def main(args, fileName):
    img1 = cv2.imread(fileName)
    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    imagesMatches = []
    imageDescriptors = []
    imageKeypoints = []
    images = []
    start = time.time()
    imageIndex = 0
    for subject in range(40):
        for imageNumber in range(10):
            selectedImage = cv2.imread('./archive/s%s/%s.pgm' % (str(subject+1), str(imageNumber+1)))
            selectedImgKP, selectedImgDsp = sift.detectAndCompute(selectedImage, None)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            imageMatches = bf.match(descriptors_1, selectedImgDsp)
            imageMatches = sorted(imageMatches, key=lambda x:x.distance)
            #Agrega imagen a arreglo
            images.append(selectedImage)
            imageKeypoints.append(selectedImgKP)
            imageDescriptors.append(selectedImgDsp)
            imagesMatches.append(imageMatches)

    matchedImage = -1
    matchedImageMatches = -1
    sujeto = -1
    for imageNumberToEvalute in range(len(images)):
        if(len(imagesMatches[imageNumberToEvalute]) > matchedImageMatches):
            matchedImage = imageNumberToEvalute
            matchedImageMatches = len(imagesMatches[imageNumberToEvalute])
            sujeto = (matchedImage+1)//10

    print('La imagen %s contiene el mayor numero de coincidencias que es %s.' % (matchedImage, matchedImageMatches))

    matches = imagesMatches[matchedImage]
    end = time.time()
    print("Tiempo de ejecucion para la deteccion del rostro %s" % (end-start))
    matched_img = np.concatenate((img1, images[matchedImage]), axis=1)
    #matched_img = cv2.drawMatches(img1, keypoints_1, images[matchedImage], imageKeypoints[matchedImage], matches[:50], images[matchedImage], flags=2)
    
    #cv2.imshow('image', matched_img)
    #cv2.putText(img=matched_img, text="STIF", org=(0,0), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    sujetoTexto = "Sujeto " + str(sujeto+1)
    return images[matchedImage], (end-start), sujetoTexto

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def evaluatingPhoto(image):
    img1 = image
    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    imagesMatches = []
    imageDescriptors = []
    imageKeypoints = []
    images = []
    start = time.time()
    imageIndex = 0
    for subject in range(40):
        for imageNumber in range(10):
            selectedImage = cv2.imread('./archive/s%s/%s.pgm' % (str(subject+1), str(imageNumber+1)))
            selectedImgKP, selectedImgDsp = sift.detectAndCompute(selectedImage, None)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            imageMatches = bf.match(descriptors_1, selectedImgDsp)
            imageMatches = sorted(imageMatches, key=lambda x:x.distance)
            #Agrega imagen a arreglo
            images.append(selectedImage)
            imageKeypoints.append(selectedImgKP)
            imageDescriptors.append(selectedImgDsp)
            imagesMatches.append(imageMatches)
    matchedImage = -1
    matchedImageMatches = -1
    sujeto = -1
    for imageNumberToEvalute in range(len(images)):
        if(len(imagesMatches[imageNumberToEvalute]) > matchedImageMatches):
            matchedImage = imageNumberToEvalute
            matchedImageMatches = len(imagesMatches[imageNumberToEvalute])
            sujeto = (matchedImage+1)//10

    #print('La imagen %s contiene el mayor numero de coincidencias que es %s.' % (matchedImage, matchedImageMatches))

    return sujeto

distortions = ['_brightness_','_distortion_affine1_', '_distortion_affine2_', '_distortion_arc1_', '_distortion_arc2_', '_scale_']

def testingMatrix():
    generalScores = []
    print("Iniciando evaluacion en matriz")
    (faces, labels) = loadingFaces.loadDataSet()
    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels.sort()
    split = train_test_split(faces, faces, labels, test_size=0.90, stratify=labels, random_state=42)
    (origTrain, origTest, trainX, testX, trainY, testY) = split
    predicciones = []
    for face in testX:
        result = evaluatingPhoto(face)
        print("Imagen predecida %s" % (result))
        predicciones.append(result)
    print("Precision sin distorsiones")
    print(accuracy_score(testY, predicciones))
    generalScores.append(accuracy_score(testY, predicciones))
    for distortion in distortions:
        (faces2, labels2) = loadingFaces.loadModifiedDataSetNew(distortion)
        labels2 = le.fit_transform(labels2)
        labels2.sort()
        prediccionesMod = []
        print("Tamanio de TestX: %s Tamanio de TextY: %s" % (len(testX), len(testY)))
        print("Tamanio de TestX: %s Tamanio de TextY: %s" % (len(faces2), len(labels2)))
        for face in faces2:
            result = evaluatingPhoto(face)
            print("Imagen predecida %s" % (result))
            prediccionesMod.append(result)
            predicciones.append(result)
        print("Precision con distorsion %s" % (distortion))
        print(accuracy_score(labels2, prediccionesMod))
        generalScores.append(accuracy_score(labels2, prediccionesMod))
    return generalScores, predicciones

if __name__ == '__main__':
    main()


