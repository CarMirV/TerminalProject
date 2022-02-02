from numpy.lib.npyio import load
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from skimage.exposure import rescale_intensity
import numpy as np
import argparse
import imutils
import time
import cv2
import os


def loadDataSet():
    loadedFaces = []
    loadedLabels = []
    for subject in range(40):
        for imageNumber in range(10):
            selectedImage = cv2.imread('./archive/s%s/%s.pgm' % (str(subject+1), str(imageNumber+1)))
            loadedFaces.append(selectedImage)
            loadedLabels.append('subject%s' % (str(subject+1)))
    loadedFaces = np.array(loadedFaces)
    loadedLabels = np.array(loadedLabels)
    return (loadedFaces,loadedLabels)

print("Inicializando deteccion con algoritmo Eigenfaces")
(faces, labels) = loadDataSet()
print("Las imagenes de la base de datos han sido cargadas")
print(len(faces))

pcaFaces = np.array([f.flatten() for f in faces])
print(len(pcaFaces))
le = LabelEncoder()
labels = le.fit_transform(labels)
print(len(labels))
split = train_test_split(faces, pcaFaces, labels, test_size=0.25, stratify=labels, random_state=42)
(origTrain, origTest, trainX, testX, trainY, testY) = split
print("Cantidad de imagenes en test %s" % (len(origTest)))
print("Construyendo eigenfaces")
pca = PCA(svd_solver="randomized", n_components=150, whiten=True)
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

media = pca.mean_.reshape((400, 64))
media = rescale_intensity(media, out_range=(0,255))
cv2.imshow("Media", media)
cv2.imshow("Componentes", display)
cv2.waitKey(0)

print("Iniciando entrenamiento de clasificador")
model = SVC(kernel="rbf", C=10.0, gamma=0.001, random_state=42)
model.fit(trainX,trainY)

print("Evaluando el modelo")
predicciones = model.predict(pca.transform(testX))
print(classification_report(testY,predicciones, target_names=le.classes_))

idxs = np.random.choice(range(0, len(testY)), size=10, replace=False)
for i in idxs:
	predName = le.inverse_transform([predicciones[i]])[0]
	actualName = le.classes_[testY[i]]
	face = np.dstack([origTest[i]] * 3)
	face = imutils.resize(face, width=250)
	#cv2.putText(face, "pred: {}".format(predName), (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
	#cv2.putText(face, "actual: {}".format(actualName), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
	print("prediccion: {}, valor esperado: {}".format(predName, actualName))
	cv2.imshow("Face", face)
	cv2.waitKey(0)
