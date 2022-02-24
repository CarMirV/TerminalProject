#Implementando el algoritmo STIF para etraccion de key features
import cv2

def main(args, fileName):
    img1 = cv2.imread(fileName)
    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    imagesMatches = []
    imageDescriptors = []
    imageKeypoints = []
    images = []

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
    for imageNumberToEvalute in range(len(images)):
        if(len(imagesMatches[imageNumberToEvalute]) > matchedImageMatches):
            matchedImage = imageNumberToEvalute
            matchedImageMatches = len(imagesMatches[imageNumberToEvalute])

    print('La imagen %s contiene el mayor numero de coincidencias que es %s.' % (matchedImage, matchedImageMatches))

    matches = imagesMatches[matchedImage]
    matched_img = cv2.drawMatches(img1, keypoints_1, images[matchedImage], imageKeypoints[matchedImage], matches[:50], images[matchedImage], flags=2)

    cv2.imshow('image', matched_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


