# Image-Processing

How to use:



Notes:

Gaussian blur

  Began by brute forcing the blur. Looped through each pixel in image, then through each surrounding pixel to get weighted average for that one pixel. 
  This was obviously extremely slow.
  Switched to building a 2D Gaussian kernel then using scipy's convolute2D function to convolve with the image. This was much faster.
  To further decrease time complexity, I divided the blur into two passes, convoluting with a 1D Gaussian kernel first, then again with its transpose. As the convolution   of the 1D Gaussian kernel and its transpose is the 2D Gaussian kernel, using the two passes gave the same results as one. 
  Time complexity was reduced from O(kernel width * kernel height * image width * image height) to O(kernel width * image width * image height).
  I used OpenCV's cv2.getTickCount to compare the computational costs of the different methods. 
  
Edge detection


