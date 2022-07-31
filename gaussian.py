import numpy as np
from PIL import Image
import math

def GaussianBlur(sigma, radius, img_filename):
    """
    sigma: Standard Deviation of the Gaussian Function
    radius: Height of the kernel
    img_filename: Name of the image to be blurred
    returns: Greyscale image with Gaussian Blur applied as an array
    """
    def gaussian(d, sigma):
        """
        d: distance pixel is away from center
        sigma: standard deviation of the Gaussian distribution
        returns: Value of gaussian function at d
        """
        return (1/math.sqrt(2*math.pi*sigma**2)) * math.exp(-d**2/(2*sigma**2))      

    # Open image and convert to greyscale    
    img = Image.open(img_filename).convert('L')
    # Store image as an array
    img_data = np.asarray(img)
    # Make new empty image
    img_blurred = np.empty((img.height,img.width))
    # Iterate through rows
    for x in range(img.height):
        # Iterate through columns
        for y in range(img.width):
            # Set kernel sum to 0
            ker_sum = 0.0
            # Set value to 0
            val = 0.0
            n = 0
            # ------ Apply first pass ------ #
            # Iterate from 3 sigma left to 3 sigma right
            for d1 in range(math.floor(-3*radius), math.ceil(3*radius)):
                for d2 in range(math.floor(-3*radius), math.ceil(3*radius)):
                    # Calculate the distance for the gaussian
                    d = math.sqrt(d1**2 + d2**2)
                    n += 1
                    # print(f'n = {n}')
                    # print(gaussian(d, sigma))
                    # print(val)
                    # print(img_data[x+d1,y+d2])
                    try:
                        val += img_data[x+d1,y+d2] * gaussian(d, sigma)
                        #print(111111)
                    except:
                        try:
                            val += img_data[x+d1,y] * gaussian(d, sigma)
                            #print(2222222)
                        except:
                            try:
                                val += img_data[x,y+d2] * gaussian(d, sigma)
                                #print(333333)
                            except:
                                val += img_data[x,y] * gaussian(d, sigma)     
                                #print(444444)               
                
                # Add gaussian to ker_sum
                ker_sum += gaussian(d, sigma)
            # Divide value by kernel sum
            val /= ker_sum
            print(f'ker: {ker_sum}')
            # Add value to new image array
            img_blurred[x,y] = val
    return img_blurred


print("Blurring image...")
blurred_image = GaussianBlur(5, 1, 'test_image.jpg')
Image.fromarray(blurred_image).show()

    
    