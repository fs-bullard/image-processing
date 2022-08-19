import numpy as np
import cv2
import math
from PIL import Image

# Helper functions
def gauss_func_2D(sigma, x, y):
            """
            sigma: Standard deviation of the Gaussian function
            x: distance from centre of kernel
            Returns: value of Gaussian function at x from the center
            """
            return ((1/(2*np.pi*sigma**2))) * np.exp((-x**2 - y**2)/(2*sigma**2))

def build2DKernel(sigma):
    # Define radius as ceil(3 * sigma)
    radius = math.ceil(3*sigma)
    # Create array of zeros dimension (2* radius + 1, 2*radius + 1)
    kernel = np.zeros((2*radius + 1, 2*radius + 1))
    # Set kernel sum to 0
    kernelSum = 0.0
    # Iterate i from -radius to radius inclusive
    for i in range(2*radius+1):
        # Iterate j from - radius to radius inclusive
        for j in range(2*radius+1):
            # Set the (i,j)th element to the value of Gauss fn at this point
            kernel[i,j] = gauss_func_2D(sigma, i-radius, j-radius)
            # Add value of gauss function at i,j to kernelSum
            kernelSum += gauss_func_2D(sigma, i-radius, j-radius)
    return kernel, kernelSum

def gaussBW_1p(sigma, img_name):
    '''
    Inputs:
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred greyscale image as nparray
    '''
    # --------------- Build Gaussian matrix ------------------ #
    kernel, kernelSum = build2DKernel(sigma)
    # Open image and convert to greyscale numpy array
    img = np.asarray(Image.open(img_name).convert('L'))
    # Convolve image with Gaussian kernel and divide by kernelSum to retain brightness
    img_out = cv2.filter2D(img, -1, kernel) / kernelSum
    return img_out, '1-pass Gaussian Blur Grey', True
    
def gaussRGB_1p(sigma, img_name):
    '''
    Inputs:
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred RGB image as nparray
    '''

    # --------------- Build Gaussian matrix ------------------ #
    kernel, kernelSum = build2DKernel(sigma)
    # Load image and convert to numpy array
    img = np.asarray(Image.open(img_name))
    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img), dtype=np.uint8)
    # For each channel, convolve with the kernel and divide by kernelSum to retain brightness
    for i in range(3):
        img_out[:,:,i] = cv2.filter2D(img[:,:,i], -1, kernel) / kernelSum   
    return img_out, '1-pass Gaussian Blur RGB', False

def gaussRGB(sigma, img_name):
    '''
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred RGB image as nparray
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
    img = np.asarray(Image.open(img_name))
    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img), dtype=np.uint8)

    for i in range(3):
        img_out[:,:,i] = cv2.filter2D(cv2.filter2D(img[:,:,i], -1 ,  kernel) / kernelSum , -1 , kernel.T ) / kernelSum
        # img_out[:,:,i] = signal.convolve(img_out[:,:,i], kernel_2, mode='same') / kernelSum 

    return img_out, '2-pass Gaussian Blur', False