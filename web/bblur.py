import numpy as np
import cv2 as cv
from PIL import Image

def denoise_pixel(window:np.ndarray, sigd:int, sigr:int):
    # print('Denoising')
    h, w = window.shape
    # Normalisation factor
    factor_els = []
    elements = []
    x = -w // 2
    while x < w // 2 + 1:
        y = -h // 2
        while y < h // 2 + 1:
            small_w = np.exp(-((x**2 + y**2)/ (2 * sigd**2)) - ((int(window[h//2, w//2]) - int(window[y, x]))**2) / (2 * sigr**2))
            factor_els.append(small_w)
            elements.append(window[y, x] * small_w)
            # print(window[y,x])
            y += 1
        x += 1
    wp = sum(factor_els)
    rest = sum(elements)
    # print(wp, rest)
    return int(rest / wp)
        
def bilateral(img_bytes, radius, sigd, sigr):
    """
    Input: img as bytes
    radius: radius of kernel
    sigd: standard deviation of spacial component
    sigr: standard deviation of intensity component
    """
    # Open image and convert to ndarray
    img = Image.open(img_bytes)
    img = np.asarray(img)


    h, w = img.shape
    img_out = np.zeros((h, w), dtype=np.uint8)
    
    border = radius // 2
    x = border 
    while x < w - border:
        y = border
        while y < h - border:
            # print(f'(x, y) : {(x, y)}')
            # Build window
            winx, winy = 0, 0
            window = np.zeros((radius, radius), dtype=np.uint8)
            for i in range(x - border, x + border + 1):
                for j in range(y - border, y + border + 1):
                    window[winy % radius, winx % radius] = img[j, i]
                    winy += 1
                winx += 1
            img_out[y, x] = denoise_pixel(window, sigd, sigr)
            y += 1
        x += 1
    # Return image from array (ensuring array type is uint8)
    output = Image.fromarray(img_out[border:-border,border:-border].astype(np.uint8), 'L')
    return output
