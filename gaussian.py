import numpy as np
from PIL import Image

def get_weighted_value(d,value):
    """
    d: distance pixel is away from center
    value: un-weighted value of sample pixel
    returns: weighted value
    """

# Open Image
img = Image.open("StudentCard.jpg")
# Convert image to greyscale
img_bw = img.convert("L")
# Convert grey image to array
img_data = np.asarray(img_bw)

# ------------------- Vertical Blur ------------------------ #
# Iterate through each row

    # Iterate through each column

        # Add pixel to new image as the sum of each pixel in surrounding kernel weighted by gaussian function



# ------------------- Horizontal Blur ------------------------ #
