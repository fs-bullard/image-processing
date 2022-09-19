from PIL import Image
import numpy as np
from blur import gauss
import scipy as sc
import scipy.signal as signal

def sharpen(img, amount=0.2,radius=3):
    blurred, a, b = gauss(radius, img)
    ker = img + np.subtract(img, blurred / amount) * amount
    return signal.convolve2d(img, ker)






if __name__ == '__main__':
    img = Image.open('non-web-files/kodim.jpg')
    data = np.asarray(img)


    data_out = sharpen(data, 0.7, 3)
    img_out = Image.fromarray(data_out)
    img.show()
    img_out.show()