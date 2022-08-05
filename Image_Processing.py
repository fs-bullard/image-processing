import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
from PIL import Image
from g_blur import gaussianBlur_1pass_bw, gaussianBlur_1pass_rgb, gaussianBlur_2pass_rgb



e1 = cv2.getTickCount()
# ------ Uncomment below for greyscale gaussian in 1 pass ------ #
# img, msg, isGrey = gaussianBlur_1pass_bw(3, 'elcapitan.jpg') 
# ------ Uncomment below for rgb gaussian in 1 pass ------- #
# img, msg, isGrey = gaussianBlur_1pass_rgb(3, 'elcapitan.jpg') 
# ------ Uncomment below for rgb gaussian in 2 passes ------ #
img, msg, isGrey = gaussianBlur_2pass_rgb(10, 'el_capitan.jpg') 

print(msg)
# Track how long the program takes
e2 = cv2.getTickCount()
progTime = (e2 - e1) / cv2.getTickFrequency()
print(f'Time = {progTime}')
print(f'Ticks: {e2 - e1}')

# Show image with matplotlib
# Ensure correct colour map
if isGrey:
    plt.imshow(img, cmap='gray')
else:
    plt.imshow(img)

plt.show()
