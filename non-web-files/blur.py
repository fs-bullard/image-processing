import numpy as np
import cv2
import math
from PIL import Image
import scipy.fftpack as fp
from scipy import signal
import matplotlib.pyplot as plt

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

def gauss(sigma, img):
    '''
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred image as nparray
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
    # img_pil = Image.open(img_name)
    # if img_pil.mode == 'RGB':
    #     img = np.asarray(img_pil)
    # elif img_pil.mode == 'P':
    #     img = np.asarray(img_pil.convert('L'))
    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img), dtype=np.uint8)
    # print(np.shape(img))

    # Set grayscale flag
    grey = False

    if len(np.shape(img)) == 3:
        for i in range(3):
            img_out[:,:,i] = cv2.filter2D(cv2.filter2D(img[:,:,i], -1 ,  kernel) / kernelSum , -1 , kernel.T ) / kernelSum
    elif len(np.shape(img)) < 3:
        img_out = cv2.filter2D(cv2.filter2D(img, -1 ,  kernel) / kernelSum , -1 , kernel.T ) / kernelSum
        # Set grayscale flag to True
        grey = True
    return img_out.astype(np.uint8), '2 pass gaussian blur', grey

def fftgauss(sigma, img):
    """
    sigma: Standard deviation of the normal distribution
    img_name: filename of input image
    Returns: Blurred image as nparray
    """
    img_0 = Image.open(img)
    img_0 = np.asarray(img_0, dtype=np.uint8)
    gauss_kernel = np.outer(signal.gaussian(img_0.shape[0], 5), signal.gaussian(img_0.shape[1], 5))
    print(gauss_kernel)
    freq = fp.fft2(img_0)
    freq_ker = fp.fft2(fp.ifftshift(gauss_kernel))
    convolved = freq * freq_ker
    img_1 = fp.ifft2(convolved).real
    plt.imshow(img_1, 'gray')
    plt.show()

if __name__ == '__main__':
    fftgauss(3, 'non-web-files/kodim.jpg')