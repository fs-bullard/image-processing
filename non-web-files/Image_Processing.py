import cv2
from matplotlib import pyplot as plt
from blur import gaussBW_1p, gaussRGB_1p, gauss
# from edges import edgeDetect, kerLib



e1 = cv2.getTickCount()
# ------ Uncomment below for greyscale gaussian in 1 pass ------ #
# img, msg, isGrey = gaussBW_1p(3, 'elcapitan.jpg') 
# ------ Uncomment below for rgb gaussian in 1 pass ------- #
# img, msg, isGrey = gaussRGB_1p(3, 'elcapitan.jpg') 
# ------ Uncomment below for rgb gaussian in 2 passes ------ #
img, msg, isGrey = gauss(10, 'pagoda.jpg') 

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
