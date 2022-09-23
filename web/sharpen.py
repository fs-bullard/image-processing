import numpy as np
from PIL import Image
from gblur import gauss

def sharpen(img):
    """
    applies sharpening to image and returns in same format
    """
    # Load image and convert to numpy array
    img_blurred = gauss(7, img)
    img = Image.open(img).convert('L')
    
    img_data = np.asarray(img, dtype=np.int16)
    k = 3
    img_detailed = img_data - img_blurred
    img_sharp = np.clip(img_data + img_detailed * k, 0, 255, dtype=np.int16)
    
    # Return image from array (ensuring array type is uint8)
    output = Image.fromarray(img_sharp.astype(np.uint8), 'L')
    return output

if __name__ == '__main__':
    sharpen('non-web-files/kodim.jpg').show()