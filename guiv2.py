from email.mime import image
import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter import filedialog
from PIL import Image, ImageTk
from os.path import exists
from os import remove
import matplotlib.pyplot as plt
import numpy as np
import STIF
import knn
import Eigenfaces
import cv2

fileName = ""
global resultImages
resultImages = []
showResult = False
global executionTimesStif
global executionTimesKnn
global stifPrecision
global knnPrecision
global algorithmsRunned
global stifPrecisionHistoric
global knnPrecisionHistoric
algorithmsRunned = False
stifPresicion = []
knnPrecision = []
stifPrecisionHistoric = []
knnPrecisionHistoric = []
executionTimesStif = []
executionTimesKnn = []


restultImage = './resultImage.png'

root = Tk()

root.geometry('721x498')
root.configure(background='#F0F8FF')
root.title('Testing Screen')

root.imageToEvaluate= Canvas(root, height=200, width=200)
root.imageToEvaluate.place(x=253, y=68)

def getAlgorithmsResultsDetails():
    print("El tiempo promedio de ejecucion de STIF es de %s con una precision actual en pruebas de %s" % (getAvgTime("STIF"), getPrecision("STIF")))
    print("El tiempo promedio de ejecucion de KNN es de %s con una precision actual en pruebas de %s" % (getAvgTime("KNN"), getPrecision("KNN")))
    figure, axis = plt.subplots(1,2)
    axis[0].plot([x for x in range(len(executionTimesStif))], executionTimesStif, label="STIF")
    axis[0].plot([x for x in range(len(executionTimesKnn))], executionTimesKnn, label="KNN")
    axis[0].legend()
    axis[0].set_title("T de ejecucion")
    axis[1].plot([x for x in range(len(stifPrecisionHistoric))], stifPrecisionHistoric, label="STIF")
    axis[1].plot([x for x in range(len(knnPrecisionHistoric))], knnPrecisionHistoric, label="KNN")
    axis[1].legend()
    axis[1].set_title("Precision")

    plt.show()

def getPrecision(algorithm):
    if(algorithm == "STIF"):
        if(len(stifPresicion) > 0):
            return sum(stifPresicion)/len(stifPresicion)*100
        else:
            return -1
    elif(algorithm == "KNN"):
        if(len(knnPrecision) > 0):
            return sum(knnPrecision)/len(knnPrecision)*100
        else:
            return -1

def updatePrecision(isSubject, algorithm):
    if(algorithm == "STIF"):
        if(isSubject):
            stifPresicion.append(1)
        else:
            stifPresicion.append(0)
        stifPrecisionHistoric.append(sum(stifPresicion)/len(stifPresicion))
        print(stifPresicion)
    elif(algorithm == "KNN"):
        if(isSubject):
            knnPrecision.append(1)
        else:
            knnPrecision.append(0)
        knnPrecisionHistoric.append(sum(knnPrecision)/len(knnPrecision))
        print(knnPrecision)

def getAvgTime(algorithm):
    if(algorithm == "STIF"):
        if(len(executionTimesStif) > 0):
            return sum(executionTimesStif)/len(executionTimesStif)
        else: return -1
    elif(algorithm == "KNN"):
        if(len(executionTimesKnn) > 0):
            return sum(executionTimesKnn)/len(executionTimesKnn)
        else:
            return -1

def setResultWindowState(isRunning):
    runningResultWindow = isRunning

def destroyResultImages():
    rw.destroy()
    if(exists('./resultImage1.png') and exists('./resultImage2.png')):
        remove('./resultImage1.png')
        remove('./resultImage2.png')
    resultImages.clear()
    

def runResultsWindow():
    global rw
    rw = tk.Toplevel()
    rw.geometry('800x500')
    rw.picture_file1 = PhotoImage(file = './resultImage1.png')
    rw.picture_file2 = PhotoImage(file = './resultImage2.png')
    rw.configure(background='#F0F8FF')
    rw.title('Resultados')
    Label(rw, text='Resultado Algoritmo 1', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=200, y=25)
    Label(rw, text='Resultado algoritmo 2', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=450, y=25)
    Label(rw, text=str(getAvgTime("STIF")), bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=200, y=60)
    Label(rw, text=str(getAvgTime("KNN")), bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=450, y=60)
    rw.imageToDisplay1=Canvas(rw, height=200, width=200)
    rw.imageToDisplay2=Canvas(rw, height=200, width=200)
    rw.imageToDisplay1.place(x=200, y=100)
    rw.imageToDisplay2.place(x=450, y=100)
    rw.imageToDisplay1.create_image(200, 0, anchor=NE, image=rw.picture_file1)
    rw.imageToDisplay2.create_image(200, 0, anchor=NE, image=rw.picture_file2)
    uidt1 = Label(rw, text='La imagen predecida es la esperada?', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=310)
    uidt2 = Label(rw, text='La imagen predecida es la esperada?', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=450, y=310)
    Button(rw, text='Si', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : updatePrecision(True, "STIF"))).place(x=200, y=340)
    Button(rw, text='No', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : updatePrecision(False, "STIF"))).place(x=250, y=340)
    Button(rw, text='Si', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : updatePrecision(True, "KNN"))).place(x=450, y=340)
    Button(rw, text='No', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : updatePrecision(False, "KNN"))).place(x=500, y=340)
    Button(rw, text='Obtener resultados generales', bg='#F0F8FF', font=('arial', 12, 'normal'), command=getAlgorithmsResultsDetails).place(x=400, y=380)
    rw.imageToDisplay1.update()
    rw.imageToDisplay2.update()
    rw.protocol("WM_DELETE_WINDOW", destroyResultImages)

def uploadImage():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="./", title="Seleccione la imagen a evaluar", filetypes=(("all files", "*.*"),("pgm files", "*.pgm"),("png file","*.png")))
    root.picture_file = PhotoImage(file = fileName)
    root.imageToEvaluate.create_image(200, 0, anchor=NE, image=root.picture_file)
    root.imageToEvaluate.update()
    root.update()

def buildResultImg():
    cv2.imwrite('./resultImage1.png', resultImages[0])
    cv2.imwrite('./resultImage2.png', resultImages[1])


def runSTIF(isSecondAlgorithm):
    print("Ejecutando STIF con %s" % (fileName))
    imageToDisplay, executionTime = STIF.main(args="",fileName=fileName)
    resultImages.append(imageToDisplay)
    executionTimesStif.append(executionTime)
    if(len(resultImages) > 1):
        buildResultImg()
    if(isSecondAlgorithm):
        runResultsWindow()

def runKnn(isSecondAlgorithm):
    print("Ejecutando KNN con %s" % (fileName))
    imageToDisplay, executionTime = knn.main(args="", fileName=fileName)
    resultImages.append(imageToDisplay)
    executionTimesKnn.append(executionTime)
    if(len(resultImages) > 1):
        buildResultImg()
    if(isSecondAlgorithm):
        runResultsWindow()

def runEigenfaces(isSecondAlgorithm):
    print("Ejecutando Eigenfaces con %s" % (fileName))
    imageToDisplay, executionTime = Eigenfaces.main(args="", fileName=fileName)
    resultImages.append(imageToDisplay)
    executionTimesKnn.append(executionTime)
    if(len(resultImages) > 1):
        buildResultImg()
    if(isSecondAlgorithm):
        runResultsWindow()

Label(root, text='Seleccione la imagen a evaluar', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=178, y=14)

Button(root, text='Seleccionar imagen', bg='#F0F8FF', font=('arial', 12, 'normal'), command=uploadImage).place(x=415, y=15)

Label(root, text='Seleccione los algoritmos a evaluar', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=229, y=268)

Label(root, text='Algoritmo 1', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=98, y=274)

Label(root, text='Algoritmo 2', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=488, y=276)

algorithms1 = StringVar(root)
algorithms1.set("Seleccione un algoritmo")
algorithms2 = StringVar(root)
algorithms2.set("Seleccione un algoritmo")
def getSelection():
    print("Segun la configuracion seleccionada se evaluara el algoritmo %s contra %s" % (algorithms1.get(), algorithms2.get()))
    if(algorithms1.get() == "STIF"):
        runSTIF(False)
    elif(algorithms1.get() == "KNN"):
        runKnn(False)
    elif(algorithms1.get() == "Eigenfaces"):
        runEigenfaces(False)
    if(algorithms2.get() == "STIF"):
        runSTIF(True)
    elif(algorithms2.get() == "KNN"):
        runKnn(True)
    elif(algorithms1.get() == "Eigenfaces"):
        runEigenfaces(True)
dropDown1 = OptionMenu(root, algorithms1, "STIF", "Eigenfaces", "KNN")
dropDown1.place(x=98,y=306)
dropDown2 = OptionMenu(root, algorithms2, "STIF", "Eigenfaces", "KNN")
dropDown2.place(x=485,y=306)

Button(root, text='Iniciar evaluacion', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : getSelection())).place(x=261, y=408)

root.mainloop()

