from fileinput import filename
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
from scipy import signal
from PIL import Image

def gaussianBlur_1pass_bw(sigma, img_name):
    '''
    Inputs:
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred greyscale image as nparray
    '''
    def gauss_func_2D(sigma, x, y):
            """
            sigma: Standard deviation of the Gaussian function
            x: distance from centre of kernel
            Returns: value of Gaussian function at x from the center
            """
            return ((1/(2*np.pi*sigma**2))) * np.exp((-x**2 - y**2)/(2*sigma**2))

    # --------------- Build Gaussian matrix ------------------ #
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
            # Add value of Gauss fn at this point to kernel sum
            kernelSum += gauss_func_2D(sigma, i-radius, j-radius)
    # Open image and convert to greyscale numpy array
    img = np.asarray(Image.open(img_name).convert('L'))
    # Convolve image with Gaussian kernel and divide by kernelSum to retain brightness
    img_out = signal.convolve2d(img, kernel, boundary='symm', mode='same') / kernelSum
    return img_out

def gaussianBlur_1pass_rgb(sigma, img_name):
    '''
    Inputs:
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred RGB image as nparray
    '''
    def gauss_func_2D(sigma, x, y):
            """
            sigma: Standard deviation of the Gaussian function
            x: distance from centre of kernel
            Returns: value of Gaussian function at x from the center
            """
            return ((1/(2*np.pi*sigma**2))) * np.exp((-x**2 - y**2)/(2*sigma**2))

    # --------------- Build Gaussian matrix ------------------ #
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
    # Load image and convert to numpy array
    img = np.asarray(Image.open(img_name))
    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img), dtype=np.uint8)
    # For each channel, convolve with the kernel and divide by kernelSum to retain brightness
    for i in range(3):
        img_out[:,:,i] = cv2.filter2D(img[:,:,i], -1, kernel) / kernelSum   
    return img_out

def gaussianBlur_2pass_rgb(sigma, img_name):
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
    kernel = np.zeros(2*radius + 1)
    print(kernel)
    print('-------------------')
    print(np.transpose(kernel))
    print('-------------------')
    print(kernel.T)
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
        img_out[:,:,i] = cv2.filter2D(cv2.filter2D(img[:,:,i], -1 ,  kernel) / kernelSum , -1 , np.transpose(kernel)) / kernelSum
        # img_out[:,:,i] = signal.convolve(img_out[:,:,i], kernel_2, mode='same') / kernelSum 

    return img_out


e1 = cv2.getTickCount()
# ------ Uncomment below for greyscale gaussian in 1 pass ------ #
# img = gaussianBlur_1pass_bw(3, 'el_capitan.jpg') 
# ------ Uncomment below for rgb gaussian in 1 pass ------- #
img = gaussianBlur_1pass_rgb(3, 'elcapitan.jpg') 
# ------ Uncomment below for rgb gaussian in 2 passes ------ #
# img = gaussianBlur_2pass_rgb(1, 'elcapitan.jpg') 

# Track how long the program takes
e2 = cv2.getTickCount()
progTime = (e2 - e1) / cv2.getTickFrequency()
print(f'Time = {progTime}')
print(f'Ticks: {e2 - e1}')

# Show image with matplotlib
plt.imshow(img)
plt.show()
