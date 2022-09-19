import numpy as np
import cv2
import math
from PIL import Image
import os

def gauss(sigma, img):
    '''
    sigma: Standard deviation of the normal distribution
    img: input image as bytes
    Returns: Blurred image as PIL image
    '''
    def gauss_func_1D(sigma, x):
            """
            sigma: Standard deviation of the Gaussian function
            x: distance from centre of kernel
            Returns: value of Gaussian function at x from the center
            """
            return (np.sqrt(1/(2*np.pi*sigma**2))) * np.exp((-x**2)/(2*sigma**2))
    
    # --------------- Build Gaussian matrix ------------------ #
    # Define radius as ceil(3 * sigma)
    radius = math.ceil(3*sigma)

    # Create array of zeros dimension (2* radius + 1, 2*radius + 1)
    kernel = np.zeros((2*radius + 1,1))

    # Set kernel sum to 0
    kernelSum = 0.0

    # Iterate i from -radius to radius inclusive
    for i in range(2*radius+1):
        # Set the (i,j)th element to the value of Gauss fn at this point
        kernel[i] = gauss_func_1D(sigma, i-radius)

        # Add value of gauss fn at i,j to kernelSum
        kernelSum += gauss_func_1D(sigma, i-radius)

    # Load image and convert to numpy array
    img = Image.open(img)
    
    img_data = np.asarray(img)

    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img_data), dtype=np.uint8)

    img_out = cv2.filter2D(cv2.filter2D(img_data, -1 ,  kernel) / kernelSum , -1 , kernel.T ) / kernelSum
    img_mode='L'

    # Return image from array (ensuring array type is uint8)
    output = Image.fromarray(img_out.astype(np.uint8), img_mode)
    return output
