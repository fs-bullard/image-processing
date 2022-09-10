import numpy as np
import math
from PIL import Image

def median_of_medians(A, i):
    '''
    Inputs:
    A: list of integers
    i: index of number to find
    Returns:
    ith smallest number in A
    '''
    # Divide A into sublists of length 5
    sublists = [A[j:j+5] for j in range(0, len(A), 5)]
    # Sort each sublist and add median to medians
    medians = [sorted(sublist)[math.floor(len(sublist)/2)] for sublist in sublists]
    # Find median of median list
    if len(medians) <= 5:
        pivot = sorted(medians)[math.floor(len(medians)/2)]
    else:
        # The pivot is in the median of the medians
        pivot = median_of_medians(medians, math.floor(len(medians)/2))
    # For each element in A, if it's < or > pivot put to the left/right 
    left = [j for j in A if j < pivot]
    right = [j for j in A if j >= pivot]
    # Find index of pivot in new list
    k = len(left)
    # If index > i
    if k > i:
        # Apply median of medians to left side of list
        return median_of_medians(left, i)
    # If index < i
    if k < i:
        # Apply median of medians to right side of list
        return median_of_medians(right, i-k-1)
    else:
        return pivot
    
def get_median(A):
    '''
    Input: list of integers 
    Returns: Approximate median of the list
    '''
    return np.median(A)     # In practice, as numpy is already compiled this is faster
    return median_of_medians(A, math.floor(len(A)/2))

def median_filter(data, width):
    '''
    Input: 
    data: image as bytes
    width: width of filter window
    Return:
    nparrray image
    '''
    
    # Load image and convert to numpy array
    img_data = Image.open(data)
    # If image mode is 'P' convert type to 'L' 
    if img_data.mode == 'P':
        img_data = img_data.convert('L')
    img = np.asarray(img_data)

    shape = (img.shape[0] - width + 1, img.shape[1] - width + 1, width, width)    

    def filter_channel(img, shape):
        '''
        Input:
        img: image channel as nparray
        Return:
        filtered channel 
        '''
        strides = 2 * img.strides
        patches = np.lib.stride_tricks.as_strided(img, shape=shape, strides=strides)
        patches = patches.reshape(-1, width, width)
        windows = []

        for window in patches:
            A = []
            for i in range(len(window)):
                for j in window[i]:
                    A.append(j)
            windows.append(A)
        img_tmp = np.array([get_median(window) for window in windows])
        img_shape = (shape[0], shape[1])
        img_out = np.reshape(img_tmp, img_shape)
        return img_out

    # If image is RGB filter each channel individually
    if len(np.shape(img)) == 3:
        img_out = np.zeros((shape[0], shape[1], 3), dtype=np.uint8)
        for i in range(3):
            img_out[:,:,i] = filter_channel(img[:,:,i], shape)
        img_mode= 'RGB'

    # Else if image is greyscale only one channel to filter
    elif len(np.shape(img)) < 3:
        img_out = filter_channel(img, shape)
        img_mode='L'
    
    return Image.fromarray(img_out.astype(np.uint8), img_mode)





