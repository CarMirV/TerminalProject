import cv2
import numpy as np

def loadDataSet():
    loadedFaces = []
    loadedLabels = []
    for subject in range(40):
        for imageNumber in range(10):
            selectedImage = cv2.imread('./archive/s%s/%s.pgm' % (str(subject+1), str(imageNumber+1)))
            loadedFaces.append(selectedImage)
            loadedLabels.append('%s' % (str(subject+1)))
    loadedFaces = np.array(loadedFaces)
    loadedLabels = np.array(loadedLabels)
    return (loadedFaces,loadedLabels)

distortionFileName = ['_brightness_','_distortion_affine1_', '_distortion_affine2_', '_distortion_arc1_', '_distortion_arc2_', '_scale_']

def loadModifiedDataSet(imageDistortion):
    loadedFaces = []
    loadedLabels = []
    for subject in range(40):
        for i in range(10):
            selectedImage = cv2.imread('./archive/modifications/%s%s%s.pgm' % (str(subject+1), imageDistortion, str(i+1)))
            resized = cv2.resize(selectedImage, (92,112), interpolation = cv2.INTER_AREA)
            #print('./archive/modifications/%s%s%s.pgm' % (str(subject+1), imageDistortion, str(i+1)))
            loadedFaces.append(resized)
            loadedLabels.append('%s' % (str(subject+1)))
    loadedFaces = np.array(loadedFaces)
    loadedLabels = np.array(loadedLabels)
    return (loadedFaces,loadedLabels)

def loadModifiedDataSetNew(imageDistortion):
    loadedFaces = []
    loadedLabels = []
    for subject in range(40):
        for i in range(10):
            selectedImage = cv2.imread('./archive/modifications/%s%s%s.pgm' % (str(subject+1), imageDistortion, str(i+1)))
            resized = cv2.resize(selectedImage, (92,112), interpolation = cv2.INTER_AREA)
            #print('./archive/modifications/%s%s%s.pgm' % (str(subject+1), imageDistortion, str(i+1)))
            loadedFaces.append(resized)
            loadedLabels.append('%s' % (str(subject+1)))
    loadedFaces = np.array(loadedFaces)
    loadedLabels = np.array(loadedLabels)
    return (loadedFaces,loadedLabels)