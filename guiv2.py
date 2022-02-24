from email.mime import image
import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter import filedialog
import STIF
import knn

fileName = ""

root = Tk()

root.geometry('721x498')
root.configure(background='#F0F8FF')
root.title('Testing Screen')

root.imageToEvaluate= Canvas(root, height=200, width=200)
root.imageToEvaluate.place(x=253, y=68)

def uploadImage():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="./", title="Seleccione la imagen a evaluar", filetypes=(("all files", "*.*"),("pgm files", "*.pgm"),("png file","*.png")))
    root.picture_file = PhotoImage(file = fileName)
    root.imageToEvaluate.create_image(200, 0, anchor=NE, image=root.picture_file)
    root.imageToEvaluate.update()
    root.update()

def runSTIF():
    print("Ejecutando STIF con %s" % (fileName))
    STIF.main(args="",fileName=fileName)

def runKnn():
    print("Ejecutando KNN")
    knn.main(args="", fileName=fileName)

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
        runSTIF()
    elif(algorithms1.get() == "KNN"):
        runKnn()
    if(algorithms2.get() == "STIF"):
        runSTIF()
    elif(algorithms2.get() == "KNN"):
        runKnn()
dropDown1 = OptionMenu(root, algorithms1, "STIF", "Eigenfaces", "KNN")
dropDown1.place(x=98,y=306)
dropDown2 = OptionMenu(root, algorithms2, "STIF", "Eigenfaces", "KNN")
dropDown2.place(x=485,y=306)

Button(root, text='Iniciar evaluacion', bg='#F0F8FF', font=('arial', 12, 'normal'), command=(lambda : getSelection())).place(x=261, y=408)

root.mainloop()
