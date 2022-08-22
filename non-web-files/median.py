from statistics import median
import numpy as np
import cv2
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
    print(f'A: {A}')
    print(f'medians - {medians}')
    # Find median of median list
    if len(medians) <= 5:
        pivot = sorted(medians)[math.floor(len(medians)/2)]
    else:
        # The pivot is in the median of the medians
        pivot = median_of_medians(medians, math.floor(len(medians)/2))
    # For each element in A, if it's < or > pivot put to the left/right 
    left = [j for j in A if j < pivot]
    right = [j for j in A if j >= pivot]
    print(f'Pivot: {pivot}')
    print(f'{left} | {pivot} | {right}')
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
    return median_of_medians(A, math.floor(len(A)/2))

def median_filter(img, width):
    '''
    '''
    

    # Load image and convert to numpy array
    img = Image.open(img)
    # If image mode is 'P' convert type to 'L' 
    if img.mode == 'P':
        img = img.convert('L')
    img_data = np.asarray(img)

    # Create an empty image as numpy array
    img_out = np.zeros(np.shape(img_data), dtype=np.uint8)

    

