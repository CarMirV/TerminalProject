#Implementando el algoritmo STIF para etraccion de key features
import cv2
import time
import numpy as np

def main(args, fileName):
    img1 = cv2.imread(fileName)
    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    imagesMatches = []
    imageDescriptors = []
    imageKeypoints = []
    images = []
    start = time.time()
    imageIndex = 0
    for subject in range(40):
        for imageNumber in range(10):
            selectedImage = cv2.imread('./archive/s%s/%s.pgm' % (str(subject+1), str(imageNumber+1)))
            selectedImgKP, selectedImgDsp = sift.detectAndCompute(selectedImage, None)
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
            imageMatches = bf.match(descriptors_1, selectedImgDsp)
            imageMatches = sorted(imageMatches, key=lambda x:x.distance)
            #Agrega imagen a arreglo
            images.append(selectedImage)
            imageKeypoints.append(selectedImgKP)
            imageDescriptors.append(selectedImgDsp)
            imagesMatches.append(imageMatches)

    matchedImage = -1
    matchedImageMatches = -1
    sujeto = -1
    for imageNumberToEvalute in range(len(images)):
        if(len(imagesMatches[imageNumberToEvalute]) > matchedImageMatches):
            matchedImage = imageNumberToEvalute
            matchedImageMatches = len(imagesMatches[imageNumberToEvalute])
            sujeto = (matchedImage+1)/10

    print('La imagen %s contiene el mayor numero de coincidencias que es %s.' % (matchedImage, matchedImageMatches))

    matches = imagesMatches[matchedImage]
    end = time.time()
    print("Tiempo de ejecucion para la deteccion del rostro %s" % (end-start))
    matched_img = np.concatenate((img1, images[matchedImage]), axis=1)
    #matched_img = cv2.drawMatches(img1, keypoints_1, images[matchedImage], imageKeypoints[matchedImage], matches[:50], images[matchedImage], flags=2)

    #cv2.imshow('image', matched_img)
    #cv2.putText(img=matched_img, text="STIF", org=(0,0), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    sujetoTexto = "Sujeto " + str(sujeto)
    return matched_img, (end-start), sujetoTexto

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


