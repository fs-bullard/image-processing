import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


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

def dumb_bilateral(img:cv.Mat, d, sigd, sigr):
    print('Applying dumb bilateral filter')
    h, w = img.shape
    img_out = np.zeros((h,w), dtype=np.uint8)
    radius = d
    
    x = radius // 2 
    while x < w - radius // 2:
        y = radius // 2
        while y < h - radius // 2:
            # print(f'(x, y) : {(x, y)}')
            # Build window
            winx, winy = 0, 0
            window = np.zeros((radius, radius), dtype=np.uint8)
            for i in range(x - radius // 2, x + radius // 2 + 1):
                for j in range(y - radius // 2, y + radius // 2 + 1):
                    window[winy % radius, winx % radius] = img[j, i]
                    winy += 1
                winx += 1
            img_out[y, x] = denoise_pixel(window, sigd, sigr)
            y += 1
        x += 1

    return img_out.astype(np.uint8)

if __name__ == '__main__':
    print('------------ Processing ---------------')

    img = cv.imread('anglicised-rat.jpg', cv.IMREAD_GRAYSCALE)

    img_out = dumb_bilateral(img, d=3, sigd=150, sigr=150)
    img_eg = cv.bilateralFilter(img, d=3, sigmaColor=150, sigmaSpace=150)
    fig1 = plt.figure('mine')
    plt.imshow(img_out, 'gray')
    fig2 = plt.figure('not mine')
    plt.imshow(img_eg, 'gray')
    plt.show()