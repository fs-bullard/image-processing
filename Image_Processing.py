from fileinput import filename
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
from scipy import signal
from PIL import Image

def gaussianBlur_1pass_bw(sigma, img_name):
    '''
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
            kernelSum += gauss_func_2D(sigma, i-radius, j-radius)
    print(kernel)
    print(f'Kernel sum = {kernelSum}')
    

    img = np.asarray(Image.open(img_name).convert('L'))
    # plt.imshow(img, cmap='gray')
    # plt.show()

    img_out = signal.convolve2d(img, kernel, boundary='symm', mode='same')


    plt.imshow(img_out, cmap='gray')
    plt.show()

def gaussianBlur_1pass_rgb(sigma, img_name):
    '''
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
            kernelSum += gauss_func_2D(sigma, i-radius, j-radius)
    print(kernel)
    print(f'Kernel sum = {kernelSum}')
    

    img = np.asarray(Image.open(img_name).convert('RGB'))
    img_r = img[:,:,0]
    img_g = img[:,:,1]
    img_b = img[:,:,2]
    # plt.imshow(img, cmap='gray')
    # plt.show()

    img_out = img.copy()

    for i in range(3):
        img_out[:,:,i] = signal.convolve2d(img[:,:,i], kernel, boundary='symm', mode='same')

    # img_r_out = signal.convolve2d(img_r, kernel, boundary='symm', mode='same')
    # img_g_out = signal.convolve2d(img_g, kernel, boundary='symm', mode='same')
    # img_b_out = signal.convolve2d(img_b, kernel, boundary='symm', mode='same')

    # img_out = (np.dstack((img_r_out, img_g_out, img_b_out))*255.999).astype(np.uint8)
    


    plt.imshow(img_out)
    plt.show()

def gaussianBlur_2pass_rgb(sigma, img_name):
    '''
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
    kernel_1 = np.zeros(2*radius + 1)
    # Set kernel sum to 0
    kernelSum = 0.0
    # Iterate i from -radius to radius inclusive
    for i in range(2*radius+1):
        # Set the (i,j)th element to the value of Gauss fn at this point
        kernel_1[i] = gauss_func_1D(sigma, i-radius)
        kernelSum += gauss_func_1D(sigma, i-radius)
    kernel_2 = np.transpose(kernel_1)
    print(kernel_1)
    print(kernel_2)
    print(f'Kernel sum = {kernelSum}')

    

    img = np.asarray(Image.open(img_name).convert('RGB'))
    img_r = img[:,:,0]
    img_g = img[:,:,1]
    img_b = img[:,:,2]
    # plt.imshow(img, cmap='gray')
    # plt.show()

    img_out = img.copy()

    for i in range(3):
        img_out[:,:,i] = signal.convolve2d(img[:,:,i], kernel_1, boundary='symm', mode='same')
        img_out[:,:,i] = signal.convolve2d(img_out[:,:,i], kernel_2, boundary='symm', mode='same')

    # img_r_out = signal.convolve2d(img_r, kernel, boundary='symm', mode='same')
    # img_g_out = signal.convolve2d(img_g, kernel, boundary='symm', mode='same')
    # img_b_out = signal.convolve2d(img_b, kernel, boundary='symm', mode='same')

    # img_out = (np.dstack((img_r_out, img_g_out, img_b_out))*255.999).astype(np.uint8)
    


    plt.imshow(img_out)
    plt.show()


e1 = cv2.getTickCount()
# gaussianBlur_1pass_rgb(3, 'elcapitan.jpg') # Uncomment for rgb gaussian in 1 pass
# gaussianBlur_1pass_bw(3, 'el_capitan.jpg') # Uncomment for greyscale gaussian in 1 pass
gaussianBlur_2pass_rgb(3, 'elcapitan.jpg') # Uncomment for rgb gaussian in 2 passes

e2 = cv2.getTickCount()
progTime = (e2 - e1) / cv2.getTickFrequency()
print(f'Time = {progTime}')
print(f'Ticks: {e2 - e1}')