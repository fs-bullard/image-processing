import cv2 as cv
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Load the image
image = cv.imread('non-web-files/barbara.png', cv.IMREAD_GRAYSCALE)

# Define the spatial kernel size
kernel_size = 5

# Create the spatial kernel
spatial_kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)

# Define the standard deviation for the color kernel
sigma_color = 100

# Create the color kernel
color_kernel = np.exp(-((image - image[:, :, None, None]) ** 2) / (2 * sigma_color ** 2))

# Apply bilateral blur to the image
blurred_image = ndimage.convolve(image, spatial_kernel[:, :, None, None] * color_kernel)

# Display the blurred image
plt.imshow(blurred_image, cmap='gray')
plt.show()

