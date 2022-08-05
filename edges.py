import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

def laplacianEdge(img, kerLib):
    ker = kerLib["Laplacian"]
    return cv2.filter2D(img, -1, ker)

def cannyEdge(img, kerLib):
    ker = kerLib["Canny"]
    return cv2.filter2D(img, -1, ker)

def prewittEdge(img, kerLib):
    ker = kerLib["Prewitt"]
    return cv2.filter2D(img, -1, ker)

def sobelEdge(img, kerLib):
    kerx = kerLib["SobelX"]
    kery = kerLib["SobelY"]
    return cv2.filter2D(cv2.filter2D(img, -1, kerx), -1, kery)

# Build kernel library
# Laplace Kernel
lapKer = np.array((
    [-1,-1,-1], 
    [-1, 8, -1], 
    [-1, -1, -1]), dtype='int')
# Canny Kernel
cannyKer = np.array((
    [-1,-1,-1], 
    [-1, 8, -1], 
    [-1, -1, -1]), dtype='int')
# Prewitt Kernel
prewKer = np.array((
    [-1,-1,-1], 
    [-1, 8, -1], 
    [-1, -1, -1]), dtype='int')
# Sobel Kernel
sobKerx = np.array((
    [-1,0,1], 
    [-2, 0, 2], 
    [-1, 0, 1]), dtype='int')
sobKery = np.array((
    [-1,-2,-1], 
    [0, 0, 0], 
    [1, 1, 1]), dtype='int')

kerLib = {"Laplacian":lapKer, "Canny":cannyKer, "Prewitt":prewKer, "SobelX":sobKerx, "SobelY":sobKery}

img = np.asarray(Image.open('pagoda.jpg').convert('L'))
#img_e = laplacianEdge(img, kerLib)
plt.imshow(cv2.Sobel(img, -1), cmap='gray')
#plt.imshow(img_e, cmap='gray')
plt.show()
    