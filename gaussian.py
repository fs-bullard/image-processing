import numpy as np
from PIL import Image
import math

def load_image(img_name):
        """
        img_name: Image filename
        Returns: Image as an array, image width, height
        """
        img = Image.open(img_name)
        img_data = np.asarray(img)
        width, height = img.size
        return img_data, width, height

def gauss_blur(img_name, sigma):
    """
    img_name: Filename of image to be blurred
    sigma: Standard deviation of the Gaussian function
    radius: Furthest distance from the centre of the kernel
    Returns: Blurred image as an array
    """
    def gauss_func(sigma, x):
        """
        sigma: Standard deviation of the Gaussian function
        x: distance from centre of kernel
        Returns: value of Gaussian function at x from the center
        """
        return (1/(2*math.pi*sigma**2)) * math.exp((-x**2)/(2*sigma**2))
        

    # ------- Form kernel ------- #
    # Set dimension of kernel 
    dim = 2*math.ceil(sigma) + 1
    # Create an empty dim x dim matrix
    kernel = np.empty((dim,dim))
    # Set kernel sum equal to 0
    ker_sum = 0
    # Set midpoint
    midpoint = math.ceil(sigma)
    # Iterate through rows
    for i in range(dim):
        # Iterate through columns
        for j in range(dim):
            # Set equal to value of Gaussian function here
            kernel[i,j] = gauss_func(sigma, math.sqrt((i-midpoint)**2 + (j-midpoint)**2))
            # Add to kernel sum
            ker_sum += kernel[i,j]
    # Get image data
    img_data, width, height = load_image(img_name)
    # Create new empty image
    img_blurred = np.zeros((height, width, 3),dtype=np.uint8)
    # Iterate through columns
    n = 0 ### counter
    for x in range(width-1):
        # Iterate through rows
        for y in range(height-1):
            # Set value to 0
            val_0, val_1, val_2 = 0.0, 0.0, 0.0
            # Iterate through the pixels around (x,y)
            for i in range(-sigma, sigma +1):
                for j in range(-sigma, sigma +1):
                    try:
                        val_0 += img_data[y+i,x+j,0] * kernel[i,j]
                        val_1 += img_data[y+i,x+j,1] * kernel[i,j]
                        val_2 += img_data[y+i,x+j,2] * kernel[i,j]
                    except:
                        try:
                            val_0 += img_data[y,x+j,0] * kernel[i,j]
                            val_1 += img_data[y,x+j,1] * kernel[i,j]
                            val_2 += img_data[y,x+j,2] * kernel[i,j]
                        except:
                            try:
                                val_0 += img_data[y+i,x,0] * kernel[i,j]
                                val_1 += img_data[y+i,x,1] * kernel[i,j]
                                val_2 += img_data[y+i,x,2] * kernel[i,j]
                            except:
                                val_0 += img_data[y,x,0] * kernel[i,j]
                                val_1 += img_data[y,x,1] * kernel[i,j]
                                val_2 += img_data[y,x,2] * kernel[i,j]                        
            img_blurred[y,x] = [val_0 / ker_sum, val_1 / ker_sum, val_2 / ker_sum]
            print(f'Original: 0: {img_data[y,x,0]} 1: {img_data[y,x,1]} 2: {img_data[y,x,2]}')
            print(f'Blurred: 0:{val_0 / ker_sum} 1: {val_1 / ker_sum} 2: {val_2 / ker_sum}')
            n += 1 ### counter
            for a in [1/8,1/4,3/8,1/2,5/8,3/4]:
                if n == a*width*height:
                    print(f'{a} complete...')
    return img_blurred

print("Blurring Image...")
img_blurred_data = gauss_blur('elcapitan.jpg', sigma = 3)
img_blurred = Image.fromarray(img_blurred_data)
img_blurred.show()



