#from cProfile import label
#from curses import window
from enum import auto
import tkinter as tk
from tkinter import Canvas, Label, OptionMenu, StringVar, font
import STIF
import Eigenfaces
import knn
from PIL import ImageTk, Image

def runSTIF():
    print("Ejecutando STIF")
    imageResult = STIF.main("test")
    imageResult = ImageTk.PhotoImage(imageResult)
    panel = Label(window, image=imageResult)
    panel.pack()
    
def runEigenfaces():
    print("Ejecutando Eigenfaces")
    Eigenfaces.main("test")

def runKnn():
    print("Ejecutando KNN")
    knn.main("test")


window = tk.Tk()
window.title("Testing window")
window.geometry("800x600")

def main():
    
    #buttonSTIF = tk.Button(window, text="STIF", width=25, command=(lambda : runSTIF()))
    #buttonSTIF.pack()
    #buttonEigenfaces = tk.Button(window, text="Eigenfaces", width=25, command=(lambda : runEigenfaces()))
    #buttonEigenfaces.pack()
    #buttonKNN = tk.Button(window, text="KNN", width=25, command=(lambda : runKnn()))
    #buttonKNN.pack()
    canvas = Canvas(window, width=800, height=200)
    canvas.create_text(400, 50, text="Seleccione los algoritmos a usar para evaluar la imagen", fill="black", font=('Helvetica 10 bold'))
    canvas.pack()
    algorithms1 = StringVar(window)
    algorithms1.set("Seleccione un algoritmo")
    algorithms2 = StringVar(window)
    algorithms2.set("Seleccione un algoritmo")
    dropDown1 = OptionMenu(window, algorithms1, "STIF", "Eigenfaces", "KNN")
    dropDown1.pack(side="left")
    dropDown2 = OptionMenu(window, algorithms2, "STIF", "Eigenfaces", "KNN")
    dropDown2.pack(side="right")
    def startExecution():
        print("Se evaluara el algoritmo %s con %s" % (dropDown1.get(), dropDown2.get()))
    selection = tk.Button(window, text="Iniciar evaluacion", width=25, command=(lambda : startExecution()))
    selection.pack()

    
    window.mainloop()

if __name__ == "__main__":
    main()

