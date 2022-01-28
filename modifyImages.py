import sys
import os.path
import random
from wand.image import Image
import mysql.connector
from mysql.connector import Error

class Distortion:
    distortion = ''
    def __init__(self,distortion,arguments):
        self.distortion = distortion
        self.arguments = arguments

distortion = [Distortion('affine',[10,10,15,15,139,0,100,20,0,92,50,80]),Distortion('affine_projection',[0.7, 0.1, 0, 0.6, 5, 5]),Distortion('arc',[15,])]



try:
    connection = mysql.connector.connect(host='localhost',database='terminalProject',user='root',password='Cmirandauammx1610!')
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS terminalProject.facesDatabase  (path VARCHAR(255), subject VARCHAR(255));")
        print("Se ha generado de manera exitosa la tabla facesDatabase")
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            for modify in distortion:
                img = random.randint(1,10)
                imgPath = path + "/" + str(img) + ".pgm"
                print(imgPath)
                with Image(filename=imgPath) as imageSelection:
                    imageSelection.distort(modify.distortion, modify.arguments)
                    print("Modificando la imagen: " + str(img) + " con el metodo: " + modify.distortion)
                    saveName = path + "/" + "distortion_" + modify.distortion + ".pgm"
                    print("Guardando la imagen con en: " + saveName)
                    imageSelection.save(filename=saveName)
                    cursor.execute("INSERT INTO facesDatabase (path, subject) VALUES ('%s','%s');" % (saveName, str(i+1)))
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            img = random.randint(1,10)
            imgPath = path + "/" + str(img) + ".pgm"
            print(imgPath)
            with Image(filename=imgPath) as imageSelection:
                imageSelection.transform('92x112','135%')
                imageSelection.crop(width=92, height=112, gravity='center')
                saveName = path + "/" + str(i+1) + "_scale.pgm"
                imageSelection.save(filename=saveName)
            img = random.randint(1,10)
            imgPath = path + "/" + str(img) + ".pgm"
            with Image(filename=imgPath) as imageSelection:
                imageSelection.brightness_contrast(-30,10,'all_channels')
                saveName = path + "/" + str(i+1) + "_brightness.pgm"
                imageSelection.save(filename=saveName)
            for imageNumber in range(10):
                cursor.execute("INSERT INTO facesDatabase (path, subject) VALUES ('%s','%s');" % (path + "/" + str(imageNumber+1), str(i+1)))
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



            
        