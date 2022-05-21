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
    def __init__(self,distortion,arguments,distortionName):
        self.distortion = distortion
        self.arguments = arguments
        self.distortionName = distortionName

distortion = [Distortion('affine',[10,10,5,5,70,10,75,5,60,60,60,65],'affine1'),
Distortion('affine',[10,10,5,5,70,10,85,15,70,92,85,72],'affine2'),
Distortion('arc',[15,],'arc1'),
Distortion('arc',[18,],'arc2')]

def testClass():
    for i in range(40):
        records = dbConnection.main(i+1)
        print("valores extraidos con el sujeto %s" % (i+1))
        for record in records:
            print(record)

try:
    connection = mysql.connector.connect(host='localhost',database='terminalProjectV2',user='root',password='cmirandauam1610!')
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS terminalProjectV2.facesDatabase  (id int NOT NULL AUTO_INCREMENT, subject VARCHAR(255), PRIMARY KEY(id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS terminalProjectV2.imagesPath (id int NOT NULL AUTO_INCREMENT, imagePath VARCHAR(255), subjectId int, modified BOOL, PRIMARY KEY(id));")
        print("Se ha generado de manera exitosa la tabla facesDatabase e imagesPath")
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            cursor.execute("INSERT INTO terminalProjectV2.facesDatabase (subject) VALUES('%s');" % ("sujeto" + str(i+1)))
            for modify in distortion:
                for j in range(10):
                    img = random.randint(1,10)
                    imgPath = path + "/" + str(img) + ".pgm"
                    print(imgPath)
                    with Image(filename=imgPath) as imageSelection:
                        imageSelection.distort(modify.distortion, modify.arguments)
                        print("Modificando la imagen: " + str(img) + " con el metodo: " + modify.distortion)
                        saveName = "./archive/modifications/" + str(i+1) + "_distortion_" + modify.distortionName + "_" + str(j+1) + ".pgm"
                        print("Guardando la imagen con en: " + saveName)
                        imageSelection.save(filename=saveName)
                        cursor.execute("INSERT INTO terminalProjectV2.imagesPath (imagePath, subjectId, modified) VALUES('%s',%s, TRUE);" % (saveName, str(i+1)))
        for i in range(40):
            print("Modificando sujeto " + str(i+1))
            path = "./archive/s" + str(i+1)
            for j in range (10):
                img = random.randint(1,10)
                imgPath = path + "/" + str(img) + ".pgm"
                print(imgPath)
                with Image(filename=imgPath) as imageSelection:
                    imageSelection.transform('112x112','135%')
                    imageSelection.crop(width=112, height=112, gravity='center')
                    saveName = "./archive/modifications/" + str(i+1) + "_scale_" + str(j+1) + ".pgm"
                    imageSelection.save(filename=saveName)
                    cursor.execute("INSERT INTO terminalProjectV2.imagesPath (imagePath, subjectId, modified) VALUES('%s',%s, TRUE);" % (saveName, str(i+1)))
            for j in range(10):
                img = random.randint(1,10)
                imgPath = path + "/" + str(img) + ".pgm"
                with Image(filename=imgPath) as imageSelection:
                    imageSelection.brightness_contrast(-30,10,'all_channels')
                    saveName = "./archive/modifications/" + str(i+1) + "_brightness_" + str(j+1) + ".pgm"
                    imageSelection.save(filename=saveName)
                    cursor.execute("INSERT INTO terminalProjectV2.imagesPath (imagePath, subjectId, modified) VALUES(\"%s\",%s, TRUE);" % (saveName, str(i+1)))
            for imageNumber in range(10):
                saveName = path + "/" + str(imageNumber + 1) + ".pgm"
                cursor.execute("INSERT INTO terminalProjectV2.imagesPath (imagePath, subjectId, modified) VALUES('%s',%s, FALSE);" % (saveName, str(i+1)))
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        connection.commit()
        cursor.close()
        connection.close()
        #testClass()
        print("MySQL connection is closed")



            
        