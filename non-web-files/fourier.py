import numpy as np
import cv2
import scipy as sc
from blur import *
import matplotlib.pyplot as plt
from skimage import data, io, filters
from skimage.color import rgb2gray

# Make test image

ncols, nrows = 120, 120
sq_size, nsq = 10, 20
image = np.zeros((nrows, ncols))
sq_locs = np.zeros((nrows, ncols), dtype=bool)
sq_locs[1:-sq_size-1:,1:-sq_size-1] = True

def place_square():
    pass





fig = plt.figure(figsize=(10,7))
rows = 2
columns = 2

img = rgb2gray(io.imread('non-web-files/test_im.jpg'))

fig.add_subplot(rows, columns, 1)
plt.imshow(img, cmap='gray')

ftimage = np.fft.fft2(img)
ftimage = np.fft.fftshift(ftimage)

fig.add_subplot(rows, columns, 2)
plt.imshow(np.abs(ftimage).astype(np.uint8), cmap='gray')

# ftimagep, a, b = gauss(sigma=5, img=ftimage.astype(np.uint8))
ftimagep = cv2.GaussianBlur(ftimage.astype(np.uint8), sigmaX=5, ksize=(0,0))
fig.add_subplot(rows, columns, 3)
plt.imshow(np.abs(ftimagep), cmap='gray')

# imagep = np.fft.ifftshift(ftimagep)
imagep = np.fft.ifft2(ftimagep)
fig.add_subplot(rows, columns, 4)
plt.imshow(np.abs(imagep), cmap='gray')




plt.show()