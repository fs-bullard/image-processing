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
        return (math.sqrt(1/(2*math.pi*sigma**2))) * math.exp((-x**2)/(2*sigma**2))
    
    def get_ker_sum(sigma, radius):
        """
        sigma: standard deviation of Gaussian function
        radius: radius of kernel
        returns: sum of gaussian values in both kernels
        """
        ker_sum = 0.0
        for i in range(-radius, radius):
            ker_sum += gauss_func(sigma,i)*2
        return ker_sum


    def hv_pass(direction, sigma, width, height, img_data):
        """
        direction: Either 'h' or 'v' where you want horizontal or vertical pass
        sigma: Standard deviation of gaussian
        width, height: width and height of image
        img_data: Image as a numpy array
        returns: Image blurred by one pass
        """
        def add_value(x,y,i,j,sigma, val_0, val_1, val_2):
            """
            x,y: coordinates of center of kernel
            i: use if h pass
            j: use if v pass
            sigma: standard deviation of gaussian
            values: the pixel values
            returns: new pixel values
            """
            val_0 += img_data[y+j,x+i,0] * gauss_func(sigma, i)
            val_1 += img_data[y+j,x+i,1] * gauss_func(sigma, i)
            val_2 += img_data[y+j,x+i,2] * gauss_func(sigma, i) 
            return val_0, val_1, val_2
        print("Applying Gaussian blur...")
        # Set kernel radius
        radius = math.ceil(3*sigma)        
        # Get kernel sum
        ker_sum = get_ker_sum(sigma, radius) 
        # Ensure only 'h' or 'v' direction
        assert direction == 'h' or direction == 'v'
        print(f'Starting {direction} pass')
        # Create new blank image
        img_blurred = np.zeros((height, width, 3),dtype=np.uint8)
        # Iterate through rows and columns
        for x in range(0,width):
            for y in range(0, height):
                # Set pixel values to 0
                val_0, val_1, val_2 = 0.0, 0.0, 0.0
                # Iterate through 1-d kernel
                for i in range(-radius, radius):
                    if direction == 'h': # Executes if horizontal pass
                        # For the border, just use the parent pixel as there are none around
                        try:
                            val_0, val_1, val_2 = add_value(x,y,i,0,sigma, val_0, val_1, val_2)
                        except:
                            val_0, val_1, val_2 = add_value(x,y,0,0,sigma, val_0, val_1, val_2)
                    elif direction =='v': # Executes if vertical pass
                        # For the border, just use the parent pixel as there are none around
                        try:
                            val_0, val_1, val_2 = add_value(x,y,0,i,sigma, val_0, val_1, val_2)
                        except:
                            val_0, val_1, val_2 = add_value(x,y,0,0,sigma, val_0, val_1, val_2)
                # Add values to image
                img_blurred[y,x] = [val_0 / ker_sum, val_1 / ker_sum, val_2 / ker_sum]
        return img_blurred

    # Get image data
    img_data, width, height = load_image(img_name)
    # First pass
    img_temp = hv_pass('h', sigma, width, height, img_data)
    Image.fromarray(img_temp).show()
    # Second pass
    img_blurred = hv_pass('v', sigma, width, height, img_temp)
    return img_blurred

def edge_detect(img_name):
    pass


### ---------Uncomment to apply Gaussian blur: ----------###
# img_blurred_data = gauss_blur('elcapitan.jpg', sigma = 3)
# img_blurred = Image.fromarray(img_blurred_data)
# img_blurred.show()
# img_blurred.save('elcapitan_blurred.png')


