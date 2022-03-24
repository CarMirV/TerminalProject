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
    root.knnCanva.create_image(100, 100, anchor=CENTER, image=root.knnImage)
    root.knnCanva.update()
    root.eigenfacesCanva.create_image(100, 100, anchor=CENTER, image=root.eigenfacesImage)
    root.eigenfacesCanva.update()
    plotValues()
    root.timeGraphImage = PhotoImage(file = './timeGraph.png')
    imageResized = root.timeGraphImage.resize((200,200), Image.ANTIALIAS)
    root.timeGraphCanva.create_image(100, 100, anchor=CENTER, image=imageResized)
    root.timeGraphCanva.update()

def startEvaluation():
    print("Iniciando evaluacion")
    stifImageRes, stifExecutionTime, stifSujeto = STIF.main(args="", fileName=fileName)
    stifExecTime.append(stifExecutionTime)
    knnImageRes, knnExecutionTime = knn.main(args="", fileName=fileName)
    knnExecTime.append(knnExecutionTime)
    eigenfacesImageRes, eigenfacesExecutionTime = Eigenfaces.main(args="", fileName=fileName)
    eigenfacesExecTime.append(eigenfacesExecutionTime)
    cv2.imwrite(stifResImgPath, stifImageRes)
    cv2.imwrite(knnResImgPath, knnImageRes)
    cv2.imwrite(eigenfacesResImgPath, eigenfacesImageRes)
    updateResultImages()
    

global root
root = Tk()
root.geometry('1200x800')
root.configure(background='#F0F8FF')
root.title('Evaluacion de algoritmos')

title = Label(root, text='Sistema de evaluación de rendimiento de algoritmos', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=50, y=10)
seleccionImagenLbl = Label(root, text='Seleccione una imagen a evaluar', bg='#F0F8FF', font=('arial', 13, 'normal')).place(x=50, y=40)
seleccionImagen = Button(root, text='Seleccionar imagen', bg='#F0F8FF', font=('arial', 12, 'normal'), command=uploadImage).place(x=50, y=70)
startButton = Button(root, text="Iniciar", bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : startEvaluation())).place(x=120,y=340)

root.imageToEvaluate=Canvas(root, height=200, width=200)
root.imageToEvaluate.place(x=50, y=130)
root.resizable(True, True)

stifLabel = Label(root, text='Resultado STIF', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=400,y=70)
root.stifCanva = Canvas(root, height=200, width=200)
root.stifCanva.place(x=400, y=100)
root.stifResLblVal = StringVar()
root.stifResLblVal.set("")
root.stifResLbl = Label(root, textvariable=root.stifResLblVal, bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=400,y=310)
knnLabel = Label(root, text='Resultado KNN', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=400,y=340)
root.knnCanva = Canvas(root, height=200, width=200)
root.knnCanva.place(x=400, y=370)
root.knnResLbl = Label(root, text='Prediccion: Sujeto X', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=400,y=580)
eigenfacesLabel = Label(root, text='Resultado Eigenfaces', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=700,y=70)
root.eigenfacesCanva = Canvas(root, height=200, width=200)
root.eigenfacesCanva.place(x=700, y=100)
root.eigenfacesResLbl = Label(root, text='Prediccion: Sujeto X', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=700,y=310)
timeLbl = Label(root, text='Tiempo promedio', bg='#F0F8FF', font=('arial', 16, 'bold')).place(x=50,y=380)
root.timeGraphCanva = Canvas(root, height=200, width=200)
root.timeGraphCanva.place(x=50,y=410)

root.mainloop()