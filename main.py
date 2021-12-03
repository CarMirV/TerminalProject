import random
from wand.image import Image

class Distortion:
    distortion = ''
    def __init__(self,distortion,arguments):
        self.distortion = distortion
        self.arguments = arguments

distortion = [Distortion('affine',[10,10,15,15,139,0,100,20,0,92,50,80]),Distortion('affine_projection',[0.7, 0.1, 0, 0.6, 5, 5]),Distortion('arc',[45,])]



for i in range(10):
    print("Modificando sujeto " + str(i+1))
    path = "./archive/s" + str(i+1)
    for modify in distortion:
        img = random.randint(1,10)
        imgPath = path + "/" + str(img) + ".pgm"
        print(imgPath)
        with Image(filename=imgPath) as imageSelection:
            imageSelection.distort(modify.distortion, modify.arguments)
            print("Modificando la imagen: " + str(img) + " con el metodo: " + modify.distortion)
            saveName = path + "/" + str(i+1) + "_distortion_" + modify.distortion + ".pgm"
            print("Guardando la imagen con en: " + saveName)
            imageSelection.save(filename=saveName)
        


#with Image(filename ="./archive/s1/1.pgm") as img:
#    img.distort('arc',(45, ))
#    img.save(filename ="1_distort.pgm")