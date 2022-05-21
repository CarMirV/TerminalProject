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
import DetailedMatches
global stifSecondImage
global stifSegundoSujeto
global stifResImgPath
global knnResImgPath
global eigenfacesResImgPath
stifResImgPath = './stifResult.png'
knnResImgPath = './knnResult.png'
eigenfacesResImgPath = './eigenfacesResult.png'
global stifExecTime
global knnExecTime
global eigenfacesExecTime
stifExecTime = []
knnExecTime = []
eigenfacesExecTime = []
global eigenClassReport
eigenClassReport = ''

global stifExp
global eigenExp
global knnExp

stifExp = "STIF es un algoritmo diseñado\npara la detección de objetos\nsin importar su orientación o\npercepción dentro de una imagen,\npor lo que este algoritmo es\nsensible a los cambios de iluminación."
knnExp = "KNN es un algoritmo que obtiene los\npuntos clave dentro de una imagen,\nlos cuales son aquellos que\nla \"describen\" y despues los compara con\naquellos en cada imagen para determinar\nsi son lo mismo, es por esto que este\nalgoritmo es sensible a la iluminación,\norientación y tamaño del rostro."
eigenExp = "Eigenfaces genera vectores descriptores\npor cada conjunto de imagenes de sujeto\npara obtener de esta manera un rostro promedio,\nes por esto que este algoritmo es mas\nsusceptible a la iluminacion\ny orientacion del rostro."


def uploadImage():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="./", title="Seleccione la imagen a evaluar", filetypes=(("all files", "*.*"),("pgm files", "*.pgm"),("png file","*.png")))
    root.picture_file = PhotoImage(file = fileName)
    root.imageToEvaluate.create_image(100, 100, anchor=CENTER, image=root.picture_file)
    root.imageToEvaluate.update()
    root.update()

def plotValues():
    stifX = [x for x in range(len(stifExecTime))]
    stifY = stifExecTime
    knnX = [x for x in range(len(knnExecTime))]
    knnY = knnExecTime
    eigenX = [x for x in range(len(eigenfacesExecTime))]
    eigenY = eigenfacesExecTime
    plt.title("T de ejecucion")
    plt.plot(stifX, stifY)
    plt.plot(knnX, knnY)
    plt.plot(eigenX, eigenY)
    plt.savefig('./timeGraph.png')
    #plt.show()

def updateResultImages():
    root.stifImage = PhotoImage(file = stifResImgPath)
    root.knnImage = PhotoImage(file = knnResImgPath)
    root.eigenfacesImage = PhotoImage(file = eigenfacesResImgPath)
    root.stifCanva.create_image(100, 100, anchor=CENTER, image=root.stifImage)
    root.stifCanva.update()
    root.update()
    root.knnCanva.create_image(100, 100, anchor=CENTER, image=root.knnImage)
    root.knnCanva.update()
    root.update()
    root.eigenfacesCanva.create_image(100, 100, anchor=CENTER, image=root.eigenfacesImage)
    root.eigenfacesCanva.update()
    root.update()

def startEvaluation():
    #Aqui debo de introducir el reporte de clasificacion 
    #Version con linea de comandos que solamente retorne una matriz de resultado
    print("Iniciando evaluacion")
    stifImageRes, stifExecutionTime, stifSujeto, stifSecondImage, stifSegundoSujeto = STIF.main(args="", fileName=fileName)
    stifExecTime.append(stifExecutionTime)
    knnImageRes, knnExecutionTime, knnSujeto = knn.main(args="", fileName=fileName)
    knnExecTime.append(knnExecutionTime)
    eigenfacesImageRes, eigenfacesExecutionTime, eigenClassReport, eigenSujeto = Eigenfaces.main(args="", fileName=fileName)
    print(eigenClassReport)
    knnSujeto = "Sujeto " + str(knnSujeto)
    eigenfacesExecTime.append(eigenfacesExecutionTime)
    root.stifSubjectLbl.config(text=stifSujeto)
    root.knnSubjectLbl.config(text=knnSujeto)
    root.eigenSubjectLbl.config(text=eigenSujeto)
    eigenSubject.set(eigenSujeto)
    cv2.imwrite(stifResImgPath, stifImageRes)
    cv2.imwrite(knnResImgPath, knnImageRes)
    cv2.imwrite(eigenfacesResImgPath, eigenfacesImageRes)
    updateResultImages()

def moreDetails():
    global detailsWindow
    detailsWindow = tk.Toplevel()
    detailsWindow.geometry('1200x800')
    detailsWindow.configure(background='#F0F8FF')
    detailsWindow.title('Mas informacion de resultados')
    stifResLbl = Label(detailsWindow, text='Resultado STIF', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=30)
    stifSubjectLbl = Label(detailsWindow, text='', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=630)
    detailsWindow.stifResCanva = Canvas(detailsWindow, height=200, width=200)
    detailsWindow.stifResCanva.place(x=55, y=50)
    detailsWindow.stifSecResCanva = Canvas(detailsWindow, height=200, width=200)
    detailsWindow.stifSecResCanva.place(x=55, y=300)
    stifSecResLbl = Label(detailsWindow, text='Segundo mejor resultado STIF', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=280)
    stifSecSubjectLbl = Label(detailsWindow, text='', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=510)
    knnResLbl = Label(detailsWindow, text='Resultado KNN', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=480,y=30)
    knnSubjectLbl = Label(detailsWindow, text='', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=630)
    detailsWindow.knnResCanva = Canvas(detailsWindow, height=200, width=200)
    detailsWindow.knnResCanva.place(x=480, y=50)
    eigenResLbl = Label(detailsWindow, text='Resultado Eigenfaces', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=905,y=30)
    eigenSubjectLbl = Label(detailsWindow, text='', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=630)
    detailsWindow.eigenResCanva = Canvas(detailsWindow, height=200, width=200)
    detailsWindow.eigenResCanva.place(x=905, y=50)
    print(eigenClassReport)
    #eigenClassRepLbl = Label(detailsWindow, text=, bg='#F0F8FF', font=('arial', 14, 'normal')).place(x=905,y=150)
    imageToEvaluate = cv2.imread(fileName)
    stifImage = cv2.imread(stifResImgPath)
    knnImage = cv2.imread(knnResImgPath)
    eigenfacesImage = cv2.imread(eigenfacesResImgPath)
    cv2.imwrite("./stifMatches.png", DetailedMatches.showDetailedMatches(imageToEvaluate, stifImage))
    cv2.imwrite("./knnMatches.png", DetailedMatches.showDetailedMatches(imageToEvaluate, knnImage))
    cv2.imwrite("./eigenMatches.png",DetailedMatches.showDetailedMatches(imageToEvaluate, eigenfacesImage))
    root.stifDetailsPicture = PhotoImage(file = 'stifMatches.png')
    root.knnDetailsPicture = PhotoImage(file = 'knnMatches.png')
    root.eigenDetailsPicture = PhotoImage(file = 'eigenMatches.png')
    detailsWindow.stifResCanva.create_image(100,100,anchor=CENTER, image=root.stifDetailsPicture)
    detailsWindow.knnResCanva.create_image(100, 100, anchor=CENTER, image=root.knnDetailsPicture)
    detailsWindow.eigenResCanva.create_image(100,100,anchor=CENTER, image=root.eigenDetailsPicture)
    stifExpLbl = Label(detailsWindow, text=stifExp, bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=40,y=300)
    knnExpLbl = Label(detailsWindow, text=knnExp, bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=460,y=300)
    eigenExpLbl = Label(detailsWindow, text=eigenExp, bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=880,y=300)
    detailsWindow.stifResCanva.update()
    detailsWindow.knnResCanva.update()
    detailsWindow.eigenResCanva.update()
    print("Getting more details")

global root
root = Tk()
root.geometry('1200x800')
root.configure(background='#F0F8FF')
root.title('Evaluacion de algoritmos')

title = Label(root, text='Sistema de evaluación de rendimiento de algoritmos de reconocimiento facial', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=50, y=10)
author = Label(root, text="Desarrollado por Carlos Daniel Miranda Viloria", bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=50, y=30)
instrucciones = Label(root, text="1.Seleccione una imagen para ser evaluada\n2.De Click en el boton de iniciar", bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=50, y=60)
seleccionImagenLbl = Label(root, text='Seleccione una imagen a evaluar', bg='#F0F8FF', font=('arial', 13, 'normal')).place(x=480, y=50)
seleccionImagen = Button(root, text='Seleccionar imagen', bg='#F0F8FF', font=('arial', 12, 'normal'), command=uploadImage).place(x=480, y=70)
startButton = Button(root, text="Iniciar", bg='#F0F8FF', font=('arial', 14, 'bold'), command=(lambda : startEvaluation())).place(x=555,y=330)

root.imageToEvaluate=Canvas(root, height=200, width=200)
root.imageToEvaluate.place(x=480, y=110)
root.resizable(True, True)

stifLabel = Label(root, text='Resultado STIF', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=55,y=390)
root.stifSubjectLbl = Label(root, text='', bg='#F0F8FF', font=('arial', 14, 'bold'))
root.stifSubjectLbl.place(x=55,y=630)
root.stifCanva = Canvas(root, height=200, width=200)
root.stifCanva.place(x=55, y=410)

knnLabel = Label(root, text='Resultado KNN', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=480,y=390)
root.knnSubjectLbl = Label(root, text='', bg='#F0F8FF', font=('arial', 14, 'bold'))
root.knnSubjectLbl.place(x=480,y=630)
root.knnCanva = Canvas(root, height=200, width=200)
root.knnCanva.place(x=480, y=410)

eigenSubject = StringVar('')
eigenfacesLabel = Label(root, text='Resultado Eigenfaces', bg='#F0F8FF', font=('arial', 14, 'bold')).place(x=905,y=390)
root.eigenSubjectLbl = Label(root, text='', bg='#F0F8FF', font=('arial', 14, 'bold'))
root.eigenSubjectLbl.place(x=905,y=630)
root.eigenfacesCanva = Canvas(root, height=200, width=200)
root.eigenfacesCanva.place(x=905, y=410)

detailsButton = Button(root, text="Mas detalles", bg='#F0F8FF', font=('arial', 14, 'bold'), command=(lambda : moreDetails())).place(x=530,y=650)



root.mainloop()