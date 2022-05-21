import sys
import os.path
import random
import cv2
from wand.image import Image
import mysql.connector
from mysql.connector import Error
import dbConnection

class Distortion:
    distortion = ''
    def __init__(self,distortion,arguments):
        self.distortion = distortion
        self.arguments = arguments

distortion = [Distortion('affine',[10,10,15,15,139,0,100,20,0,92,50,80]),Distortion('arc',[15,])]

def testClass():
    for i in range(40):
        records = dbConnection.main(i+1)
        print("valores extraidos con el sujeto %s" % (i+1))
        for record in records:
            print(record)

try:
    connection = mysql.connector.connect(host='localhost',database='terminalProject',user='root',password='cmirandauam1610!')
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS terminalProject.facesDatabase  (id int NOT NULL AUTO_INCREMENT, subject VARCHAR(255));")
        cursor.execute("CREATE TABLE IF NOT EXISTS terminalProject.imagesPath (id int NOT NULL AUTO_INCREMENT, imagePath VARCHAR(255), subjectId int);")
        print("Se ha generado de manera exitosa la tabla facesDatabase e imagesPath")
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            cursor.execute("INSERT INTO terminalProject.facesDatabase (subject) VALUES('%s');" % ("sujeto" + str(i+1)))
            for modify in distortion:
                img = random.randint(1,10)
                imgPath = path + "/" + str(img) + ".pgm"
                print(imgPath)
                with Image(filename=imgPath) as imageSelection:
                    imageSelection.distort(modify.distortion, modify.arguments)
                    print("Modificando la imagen: " + str(img) + " con el metodo: " + modify.distortion)
                    saveName = "./archive/modifications/" + str(i+1) + "distortion_" + modify.distortion + ".pgm"
                    print("Guardando la imagen con en: " + saveName)
                    imageSelection.save(filename=saveName)
                    cursor.execute("INSERT INTO terminalProject.imagesPath (imagePath, subjectId) VALUES('%s',%s);" % (saveName, str(i+1)))
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            img = random.randint(1,10)
            imgPath = path + "/" + str(img) + ".pgm"
            print(imgPath)
            with Image(filename=imgPath) as imageSelection:
                imageSelection.transform('112x112','135%')
                imageSelection.crop(width=112, height=112, gravity='center')
                saveName = path + "./archive/modifications/" + str(i+1) + "_scale.pgm"
                imageSelection.save(filename=saveName)
                cursor.execute("INSERT INTO terminalProject.imagesPath (imagePath, subjectId) VALUES('%s',%s);" % (saveName, str(i+1)))
            img = random.randint(1,10)
            imgPath = path + "/" + str(img) + ".pgm"
            with Image(filename=imgPath) as imageSelection:
                imageSelection.brightness_contrast(-30,10,'all_channels')
                saveName = "./archive/modifications/" + str(i+1) + "_brightness.pgm"
                imageSelection.save(filename=saveName)
                cursor.execute("INSERT INTO terminalProject.imagesPath (imagePath, subjectId) VALUES(\"%s\",%s);" % (saveName, str(i+1)))
            for imageNumber in range(10):
                saveName = path + "/" + str(imageNumber + 1) + ".pgm"
                cursor.execute("INSERT INTO terminalProject.imagesPath (imagePath, subjectId) VALUES('%s',%s);" % (saveName, str(i+1)))
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        connection.commit()
        cursor.close()
        connection.close()
        testClass()
        print("MySQL connection is closed")



            
        