import cv2
import time
import numpy as np

def showDetailedMatches(picture1, picture2):
    sift = cv2.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(picture1, None)
    imagesMatches = []
    imageDescriptors = []
    imageKeypoints = []
    images = []
    keypoints_2, descriptors_2 = sift.detectAndCompute(picture2, None)
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    imageMatches = bf.match(descriptors_1, descriptors_2)
    matched_img = cv2.drawMatches(picture1, keypoints_1, picture2, keypoints_2, imageMatches[:50], picture2, flags=2)
    #cv2.imshow('image', matched_img)
    return matched_img


if __name__ == '__main__':
    showDetailedMatches()