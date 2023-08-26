import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np


def nlm(img_noisy):

    img_denoised = cv.Mat(np.ndarray([]))

    cv.fastNlMeansDenoising(img_noisy, img_denoised)

    # img_denoised = img_noisy
    return img_denoised






if __name__ == "__main__":
    
    filename = "Image-Processing/non-web-files/barbara.png"

    img_noisy = plt.imread(filename)

    img_denoised = nlm(img_noisy)

    plt.imshow(img_denoised, cmap="gray")
    plt.show()

